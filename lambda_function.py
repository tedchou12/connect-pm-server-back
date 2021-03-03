from flask import Flask, render_template, make_response, redirect, request, session, url_for
from flask_cors import CORS
import os
import time
from datetime import date, datetime, timedelta
from src.pm_server.modules.config import config
from src.pm_server.modules.account import account
from src.pm_server.modules.tenant import tenant
from src.pm_server.modules.credential import credential
from src.pm_server.modules.oidc import google, microsoft, hac
from src.pm_server.modules.app_session import app_session
from src.pm_server.modules.sfdc import sfdc
from src.pm_server.modules.security import security
from src.pm_server.modules.one_garden import one_garden
from src.pm_server.modules.function import *
import json
import base64

obj_config = config()

app = Flask(__name__, static_folder=obj_config.params['static_path'], template_folder=obj_config.params['templates_path'])
app.secret_key = obj_config.params['flask_secret']

def lambda_cron() :
    return sync()

def header_template() :
    context_header = {'lang_home': lang('Home'),
                      'lang_setting': lang('Setting'),
                      'link_home': link(''),
                      'link_setting': link('setting'),
                      'link_logout': link('logout'),
                      'lang_logout': lang('Logout')}

    return context_header

@app.route('/')
def index() :
    obj_account = account()
    obj_credential = credential()
    obj_session = app_session()

    try :
        auth_code = request.headers.get('Authorization')
        token = auth_code.replace('Bearer ', '')
    except :
        token = ''


    if token != '' and obj_session.check_session(token) == True :
        obj_account.set_account(session['session_id'])
        credentials = obj_credential.list_credentials()
        list_credentials = []
        for credential_idx in credentials :
            credential_ele = {}
            credential_ele['url'] = base64.b64encode(credentials[credential_idx]['credential_url'].encode('utf-8')).decode('utf-8')
            credential_ele['username'] = base64.b64encode(credentials[credential_idx]['credential_username'].encode('utf-8')).decode('utf-8')
            credential_ele['password'] = base64.b64encode(credentials[credential_idx]['credential_password'].encode('utf-8')).decode('utf-8')
            list_credentials.append(credential_ele)

        return json.dumps({'result': True, 'data': list_credentials})

    else :
        return json.dumps({'result': False, 'data': []})

@app.route('/auth', methods=['GET', 'POST'])
def auth() :
    obj_account = account()
    obj_security = security()
    obj_session = app_session()
    oidc_google = google()
    oidc_microsoft = microsoft()
    oidc_hac = hac()

    if request.method == 'POST' :
        code = request.form['code']
        state = request.form['state']
        callback = request.form['callback']

        result = False
        if state == 'microsoft' :
            if code != '' :
                auth_data = oidc_microsoft.get_token(code, callback)
                if 'email' in auth_data and obj_account.check_account_email(auth_data['email']) == True :
                    session_hash = obj_session.save_session(session['account']['account_id'])
                    if session_hash != False :
                        data = {'pm_session': session_hash}
                        result = True
        elif state == 'google' :
            if code != '' :
                auth_data = oidc_google.get_token(code, callback)
                if 'email' in auth_data and obj_account.check_account_email(auth_data['email']) == True :
                    session_hash = obj_session.save_session(session['account']['account_id'])
                    if session_hash != False :
                        data = {'pm_session': session_hash}
                        result = True
        else :
            if code != '' :
                auth_data = oidc_hac.get_token(code, callback)
                if 'email' in auth_data and obj_account.check_account_email(auth_data['email']) == True :
                    session_hash = obj_session.save_session(session['account']['account_id'])
                    if session_hash != False :
                        data = {'pm_session': session_hash}
                        result = True

        return json.dumps({'result': result, 'data': data})

    else :

        return ''

@app.route('/login', methods=['GET', 'POST'])
def login() :
    oidc_google = google()
    oidc_microsoft = microsoft()
    oidc_hac = hac()

    login_vars = {'link_google': oidc_google.auth_url(),
                  'link_microsoft': oidc_microsoft.auth_url(),
                  'link_hac': oidc_hac.auth_url()}

    return json.dumps({'result': True, 'data': login_vars})

@app.route('/logout')
def logout() :
    obj_account = account()
    obj_session = app_session()

    auth_code = request.headers.get('Authorization')
    token = auth_code.replace('Bearer ', '')

    if token != '' and obj_session.check_session(token) == True :
        obj_account.set_account(session['session_id'])
        credentials = obj_credential.list_credentials()

        return json.dumps({'result': True, 'data': credentials})

    else :
        return json.dumps({'result': False, 'data': []})

@app.route('/forgot', methods=['GET', 'POST'])
def forgot() :
    obj_account = account()
    obj_session = app_session()

    if obj_session.check_session() == True :
        obj_account.set_account(session['session_id'])

        return redirect(link(''))
    elif request.method == 'POST' :
        account_info = obj_account.get_account_by_email(request.form['email'])
        if account_info != False :
            hash = obj_account.password_reset(account_info['account_id'])
            if hash != False :
                mailbody = 'Your Reset code is: ' + hash + '\r\nPlease visit here to reset your password: ' + obj_config.params['hostname'] + 'reset?email=' + account_info['account_email'] + '&code=' + hash
                sendmail(account_info['account_email'], 'reset_password', mailbody)
    else :
        a = ''

    context = {'resources_path': obj_config.params['resources_path'],
               'title': obj_config.params['app_name'],
               'lang_email': lang('E-mail'),
               'lang_reset_pass': lang('Reset Password'),
               'lang_login': lang('Return to Login'),
               'link_login': link('login'),
               'link_forgot': link('forgot')}

    return render_template('forgot.html', context=context)

@app.route('/reset', methods=['GET', 'POST'])
def reset() :
    obj_account = account()
    obj_session = app_session()

    val_email = ''
    val_code = ''
    if obj_session.check_session() == True :
        obj_account.set_account(session['session_id'])

        return redirect(link(''))
    elif request.method == 'POST' :
        account_info = obj_account.get_account_by_email(request.form['email'])
        if account_info != False :
            if request.form['pass'] == request.form['con_pass'] :
                obj_account.update_password(account_info['account_id'], request.form['code'], request.form['pass'])

                return redirect(link('login'))
    else :
        if request.args.get('email') != None :
            val_email = request.args.get('email')
        if request.args.get('code') != None :
            val_code = request.args.get('code')

    context = {'resources_path': obj_config.params['resources_path'],
               'title': obj_config.params['app_name'],
               'lang_password': lang('Password'),
               'lang_con_password': lang('Confirm Password'),
               'lang_code': lang('Code'),
               'lang_email': lang('E-mail'),
               'lang_reset_pass': lang('Reset Password'),
               'lang_login': lang('Return to Login'),
               'val_email': val_email,
               'val_code': val_code,
               'link_login': link('login'),
               'link_forgot': link('forgot')}

    return render_template('reset.html', context=context)

@app.route('/sync', methods=['GET'])
def sync() :
    obj_account = account()
    obj_tenant = tenant()
    obj_credential = credential()
    obj_session = app_session()
    obj_sfdc = sfdc()
    obj_one_garden = one_garden()

    if obj_sfdc.login() == True :
        # for adding sfdc tenant to tenants in db
        tenants = obj_sfdc.list_tenants()
        local_tenants = obj_tenant.list_tenants()
        exist_tenants = []
        for tenant1 in tenants :
            exist_tenants.append(tenant1['Name'])
            if tenant1['Name'] not in local_tenants :
                id = tenant1['attributes']['url'].split('/')[-1]
                obj_tenant.add_tenant(tenant1['Name'], id, tenant1['main_domain__c'], tenant1['Account_Name__c'], tenant1['environment_status__c'])

            # get other domains via one_garden to db
            domains = obj_one_garden.get_domains(tenant1['Name'])
            if domains != False :
                domains.remove(tenant1['main_domain__c'])
                obj_tenant.update_tenant_domains(tenant1['Name'], domains)

        # for deleting tenants in db not in sfdc
        for tenant1 in local_tenants :
            if tenant1 not in exist_tenants :
                obj_tenant.delete_tenant(tenant1)

        # get contract info via sfdc to db
        contracts = obj_sfdc.list_contracts()
        unique_contracts = {}
        for contract1 in contracts :
            if contract1['OneTenant__c'] in unique_contracts :
                if int(datetime.strptime(unique_contracts[contract1['OneTenant__c']]['contract_end_date__c'], '%Y-%m-%d').timestamp()) < int(datetime.strptime(contract1['contract_end_date__c'], '%Y-%m-%d').timestamp()) :
                    unique_contracts[contract1['OneTenant__c']] = contract1
            else :
                unique_contracts[contract1['OneTenant__c']] = contract1

        for contract1 in unique_contracts :
            tenant_info = obj_tenant.get_tenant_by_sfdc(contract1)
            if tenant_info != False :
                contract_data = {'end_date': unique_contracts[contract1]['contract_end_date__c'],
                                 'price': unique_contracts[contract1]['sub_total_price_sum__c'],
                                 'hac': unique_contracts[contract1]['hac_sum__c'],
                                 'hsb': unique_contracts[contract1]['hsb_sum__c'],
                                 'hdc': unique_contracts[contract1]['hdc_sum__c'],
                                 'dlp': unique_contracts[contract1]['dlp_sum__c'],
                                 'arc': unique_contracts[contract1]['archive_sum__c'],
                                 'hos': unique_contracts[contract1]['hos_sum__c']}
                obj_tenant.update_tenant_licenses(tenant_info['tenant_id'], contract_data)

        # for adding sfdc contacts to accounts in db
        contacts = obj_sfdc.list_contacts()
        local_contacts = obj_account.list_accounts()
        exist_contacts = []
        for contact1 in contacts :
            exist_contacts.append(contact1['Email'])
            id = contact1['attributes']['url'].split('/')[-1]
            if contact1['Email'] not in local_contacts :
                account_id = obj_account.add_account(id, contact1['Name'], contact1['Email'])
                account_data = {'phone': contact1['Phone']}
                obj_account.update_account(account_id, '', account_data)
            else :
                account_info = obj_account.get_account_by_email(contact1['Email'])
                account_data = {'phone': contact1['Phone']}
                obj_account.update_account(account_info['account_id'], '', account_data)

        # for deleting accounts in db not in sfdc contacts
        for contact1 in local_contacts :
            if contact1 not in exist_contacts :
                obj_account.delete_account(contact1)

        # for adding sfdc connects to contacts in db
        connects = obj_sfdc.list_connects()
        local_contacts = obj_account.list_accounts('sfdc')
        local_connects = obj_contact.list_contacts()
        exist_connects = []
        for connect in connects :
            if connect['Contact__c'] in local_contacts :
                account_info = local_contacts[connect['Contact__c']]
                connect_id = connect['attributes']['url'].split('/')[-1]
                exist_connects.append(connect_id)
                if connect_id in local_connects :
                    tenant1 = obj_tenant.get_tenant_by_sfdc(connect['OneTenant__c'])
                    contact_id = obj_contact.update_contact(connect_id, account_info['account_id'], tenant1['tenant_id'], connect['Distribution_Channel__c'], connect['support_flag__c'], connect['renewal_flag__c'], connect['emergency_flag__c'])
                else :
                    tenant1 = obj_tenant.get_tenant_by_sfdc(connect['OneTenant__c'])
                    contact_id = obj_contact.add_contact(connect_id, account_info['account_id'], tenant1['tenant_id'], connect['Distribution_Channel__c'], connect['support_flag__c'], connect['renewal_flag__c'], connect['emergency_flag__c'])

        # for deleting contacts in db not in sfdc connects
        for connect1 in local_connects :
            if connect1 not in exist_connects :
                obj_contact.delete_contact(connect1)

        return 'sync finished'

if __name__ == '__main__' :
    cors = CORS(app, resources={'*': {'origins': '*'}})
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
