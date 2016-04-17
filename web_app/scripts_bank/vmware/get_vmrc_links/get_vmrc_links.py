#!/usr/bin/python


"""
Python+Flask web-backend program for listing the VMs on an ESXi/vCenter host with direct
Virtual Machine Remote Console (vmrc) links.
Details about console version could be found here http://noshut.ru/2016/01/getting-vmrc-links-with-python/

Tested with python3.
"""

from pyVim.connect import SmartConnect, Disconnect
import atexit
import ssl

from flask import render_template, request, Blueprint, jsonify

# define dict to store information collected from VMs and 'error' messages if any
# this dict will be served to AJAX request as response
vmrc_links = {'collected_vm_info':'',
              'error':''}

def collect_vm_info(vm, args, depth=1):
    """
    Collect general information for a particular virtual machine or recurse into a folder
    with depth protection
    :param depth:
    :param args: arguments to compile vmrc link
    :param vm: Virtual Machine Object
   """
    maxdepth = 10

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > maxdepth:
            return
        vmList = vm.childEntity
        for c in vmList:
            collect_vm_info(c, depth + 1)
        return

    vm_summary = vm.summary

    vmrc_links['collected_vm_info'] += "<p><pre>" # opening paragraph and preformatted section
    vmrc_links['collected_vm_info'] += "<strong>Name       : " + vm_summary.config.name + "</strong></br>"
    vmrc_links['collected_vm_info'] += "Path       : " + vm_summary.config.vmPathName + "</strong></br>"
    guest_name = vm_summary.config.guestFullName
    if guest_name is not None:
        vmrc_links['collected_vm_info'] += "Guest      : " + guest_name + "</br>"
    vmrc_links['collected_vm_info'] += "moID       : " + vm._moId + "</br>"
    vmrc_links['collected_vm_info'] += "VMRC Link  : " + '<a href="' + "vmrc://" + args['user'] + "@" + args['host'] + ":443/?moid=" + vm._moId + '">VMRC link</a>' + "</br>"
    annotation = vm_summary.config.annotation
    if annotation is not None and annotation != "":
        vmrc_links['collected_vm_info'] += "Annotation : " + annotation + "</br>"
    vmrc_links['collected_vm_info'] += "State      : " + vm_summary.runtime.powerState + "</br>"
    if vm_summary.guest is not None:
        ip = vm_summary.guest.ipAddress
        if ip is not None and ip != "":
             vmrc_links['collected_vm_info'] += "IP         : " + ip + "</br>"
    vmrc_links['collected_vm_info'] += "</pre></p>"    # closing paragraph


def main(args):
    """
   Simple command-line program for listing the virtual machines on a system.
   """

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE

    try:
        si = SmartConnect(host=args['host'],
                          user=args['user'],
                          pwd=args['pass'],
                          port=443,
                          sslContext=context)
    except:
        vmrc_links['error'] = '<div class="alert alert-danger" role="alert"><strong>ERROR:</strong> Could not connect to the specified host using specified username or password</div>'
        return vmrc_links

    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vm_folder') or hasattr(child, 'vmFolder'):
            datacenter = child
            vm_folder = datacenter.vmFolder
            vm_list = vm_folder.childEntity
            for vm in vm_list:
                collect_vm_info(vm, args)
    return vmrc_links


###############
#### FLASK ####
###############

get_vmrc_links_bp = Blueprint('get_vmrc_links', __name__, template_folder='templates', static_folder='static',
                              static_url_path='/get_vmrc_links/static')

@get_vmrc_links_bp.route('/get_vmrc_links', methods=['GET','POST'])
def get_vmrc_links():
    if request.method == 'GET':
        return render_template('get_vmrc_links.html')

    # handle POST method from JQuery
    elif request.method == 'POST':
        print(request.form)
        getvmrc_args = {'host': request.form['vmware_ip_addr'],
                        'user': request.form['vmware_login'],
                        'pass': request.form['vmware_pass']}

        global vmrc_links
        vmrc_links = {'collected_vm_info': '',
                      'error': ''}

        # TODO: RD: add connection timeout for vm engine. Its too long in case of netw unreach.
        vm_info = main(getvmrc_args)
        return jsonify(vm_info)