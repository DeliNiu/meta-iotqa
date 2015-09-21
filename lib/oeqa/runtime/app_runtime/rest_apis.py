# -*- coding:utf8 -*-

__author__ = 'qiuzhong'
__version__ = '0.0.1'

import os
import subprocess

from oeqa.oetest import oeRuntimeTest
from oeqa.utils.decorators import tag


@tag(TestType = 'Functional Positive', FeatureID = 'IOTOS-343')
class RESTAPITest(oeRuntimeTest):
    '''
    The test case checks whether the REST APIs for Ostro OS works well.
    '''
    rest_api = 'restapis'
    files_dir = None
    rest_api_dir = None
    target_rest_api_dir = '/tmp/%s' % rest_api
    nodeunit_zip = None
    rest_api_js_files = {

        'api_system': 'nodeunit_test_api_system.js',
        'api_oic_d': 'nodeunit_test_api_oic_d.js',
        'api_oic_p': 'nodeunit_test_api_oic_p.js',
        'api_oic_res': 'nodeunit_test_api_oic_res.js',

    }

    @classmethod
    def all_files_exists(cls):
        '''
        See wether all the files exists.
        :return:
        '''
        for test_file in cls.rest_api_js_files.values():
            if not os.path.exists(os.path.join(os.path.dirname(__file__),
                                               'files', cls.rest_api,
                                               test_file)):
                return False
        return True


    @classmethod
    def setUpClass(cls):
        '''
        Copy all the JavaScript files to the target system.
        '''
        cls.files_dir = os.path.join(os.path.dirname(__file__), 'files')
        cls.rest_api_dir = os.path.join(os.path.dirname(__file__),
                                    'files', cls.rest_api).rstrip('/')

        cls.tc.target.run('rm -fr %s' % cls.target_rest_api_dir)
        cls.tc.target.run('rm -f %s.tar.gz' % cls.target_rest_api_dir)

        if os.path.exists('%s.tar.gz' % cls.rest_api_dir):
            os.remove('%s.tar.gz' % cls.rest_api_dir)

        # compress restapi directory and copy it to target device.
        proc = None
        if cls.all_files_exists():
            proc = subprocess.Popen(
                ['tar', '-czf', '%s.tar.gz' % cls.rest_api, cls.rest_api],
                cwd = cls.files_dir)
            proc.wait()

        if proc and proc.returncode == 0 and \
            os.path.exists('%s.tar.gz' % cls.rest_api_dir):
            cls.tc.target.copy_to(
                os.path.join(
                    os.path.dirname(__file__),
                                    'files',
                                    '%s.tar.gz' % cls.rest_api),
                '%s.tar.gz' % cls.target_rest_api_dir)
            cls.tc.target.run('cd /tmp/; ' \
                            'tar -xf %s.tar.gz -C %s/' % (
                                cls.target_rest_api_dir,
                                os.path.dirname(cls.target_rest_api_dir))
                            )

        # Download nodeunit from git hub
        proc = subprocess.Popen(['wget', 'https://github.com/caolan/nodeunit/archive/master.zip'],
                                cwd = cls.files_dir)
        proc.wait()

        cls.nodeunit_zip = os.path.join(os.path.dirname(__file__),
                                    'files',
                                    'master.zip')
        if os.path.exists(cls.nodeunit_zip):
            cls.tc.target.copy_to(cls.nodeunit_zip, '/tmp/master.zip')
            cls.tc.target.run('cd /tmp/; ' \
                            'unzip -oq master.zip;' \
                            'chmod +x /tmp/nodeunit-master/bin/nodeunit'
                           )

        for api, api_js in cls.rest_api_js_files.items():
            cls.tc.target.run('cd %s; node %s' % (cls.target_rest_api_dir, api_js) )


    def test_api_system_status_code(self):
        '''
        Test status code of response of  /api/system is 200
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemStatusCode' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_has_hostname(self):
        '''
        Test if the response of /api/system has hostname property.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemHostnameNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_hostname_type(self):
        '''
        Test if type of hostname property in response is a string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemHostnameType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_hostname_value(self):
        '''
        Test if value of hostname property in response is OK.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemHostnameValue' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_has_type(self):
        '''
        Test if the response of /api/system has type property.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemTypeNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_type_type(self):
        '''
        Test if type of type property in response is a string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemTypeType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_type_value(self):
        '''
        Test if value of type property in response is OK.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemTypeValue' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_has_arch(self):
        '''
        Test if the response of /api/system has arch property.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemArchNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_arch_type(self):
        '''
        Test if type of arch property in response is a string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemArchType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_arch_value(self):
        '''
        Test if value of arch property in response is OK.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemArchValue' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_has_release(self):
        '''
        Test if the response of /api/system has release property.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemReleaseNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_release_type(self):
        '''
        Test if type of release property in response is a string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemReleaseType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_release_value(self):
        '''
        Test if value of release property in response is OK.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemReleaseValue' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_has_uptime(self):
        '''
        Test if the response of /api/system has uptime property.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemUptimeNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_uptime_type(self):
        '''
        Test if type of uptime property in response is a number.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemUptimeType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_has_loadavg(self):
        '''
        Test if the response of /api/system has loadavg property.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemLoadavgNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_loadavg_type(self):
        '''
        Test if type of loadavg property in response is an array.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemLoadavgType:' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_has_totalmem(self):
        '''
        Test if the response of /api/system has totalmem property.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemTotalmemNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_totalmem_type(self):
        '''
        Test if type of totalmem property in response is a string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemTotalmemType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_totalmem_value(self):
        '''
        Test if value of totalmem property in response is OK.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemTotalmemValue' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_has_freemem(self):
        '''
        Test if the response of /api/system has freemem property.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemFreememNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_freemem_type(self):
        '''
        Test if type of freemem property in response is a string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemFreememType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_has_cpus(self):
        '''
        Test if the response of /api/system has cpus property.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemCpusNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_cpus_type(self):
        '''
        Test if type of cpus property in response is an array.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemCpusType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_system_cpus_value(self):
        '''
        Test if value of cpus property in response is OK.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemCpusValue' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])



    def test_api_system_networkinterfaces_value(self):
        '''
        Test if value of networkinterfaces property in response is OK.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiSystemNetworkInterfacesValue' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_system']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_d_status_code(self):
        '''
        Test status code of response to /api/oic/d is 200
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicDStatusCode' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_d']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_d_has_required_n(self):
        '''
        Test if the response of /api/oic/d has required property n.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicDRequiredNNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_d']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_d_required_n_type(self):
        '''
        Test if the type of n property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicDRequiredNType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_d']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_d_has_required_di(self):
        '''
        Test if the response of /api/oic/d has required property di.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicDRequiredDiNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_d']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_d_required_di_type(self):
        '''
        Test if the type of di property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicDRequiredDiType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_d']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_d_required_di_value_uuid(self):
        '''
        Test if the value of di property in response is UUID format.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicDRequiredDiUuid' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_d']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_d_has_required_icv(self):
        '''
        Test if the response of /api/oic/d has required property icv.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicDRequiredIcvNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_d']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_d_required_icv_type(self):
        '''
        Test if the type of icv property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicRequiredDIcvType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_d']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_d_optional_dmv_type(self):
        '''
        Test if the type of dmv property (if it exists) in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicDOptionalDmvType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_d']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])



    def test_api_oic_d_optional_dmv_value_csv(self):
        '''
        Test if the value of dmv property (if it exists) in response is csv format.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicDOptionalDmvCsv' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_d']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_status_code(self):
        '''
        Test status code of /api/oic/p.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPStatusCode' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_has_required_pi(self):
        '''
        Test if the response of /api/oic/pi has required property pi.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPRequiredPiNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_required_pi_type(self):
        '''
        Test if the type of pi property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPRequiredPiType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_has_required_mnmn(self):
        '''
        Test if the response of /api/oic/p has required property mnmn.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPRequiredMnmnNotNull' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_required_mnmn_type(self):
        '''
        Test if the type of mnmn property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPRequiredMnmnType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_optional_mnml_type(self):
        '''
        Test if the type of mnml property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPOptionalMnmlType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_optional_mnmo_type(self):
        '''
        Test if the type of mnmo property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPOptionalMnmoType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_optional_mndt_type(self):
        '''
        Test if the type of mndt property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPOptionalMndtType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_optional_mnpv_type(self):
        '''
        Test if the type of mnpv property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPOptionalMnpvType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_optional_mnos_type(self):
        '''
        Test if the type of mnos property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPOptionalMnosType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_optional_mnhw_type(self):
        '''
        Test if the type of mnhw property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPOptionalMnhwType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_optional_mnfv_type(self):
        '''
        Test if the type of mnfv property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPOptionalMnfvType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_optional_mnsl_type(self):
        '''
        Test if the type of mnfv property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPOptionalMnslType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_p_optional_st_type(self):
        '''
        Test if the type of st property in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicPOptionalStType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_p']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_res_status_code(self):
        '''
        Test status code of /api/oic/res.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicResStatusCode' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_res']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_res_n_type(self):
        '''
        Test if the type of n property (if it exists) in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicResNType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_res']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_res_di_type(self):
        '''
        Test if the type of di property (if it exists) in response is string.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicResDiType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_res']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_res_di_value_uuid(self):
        '''
        Test if the value of di property (if it exists) in response is UUID format.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicResDiUuid' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_res']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    def test_api_oic_res_links_type(self):
        '''
        Test if the type of links property (if it exists) in response is an array.
        '''
        (api_status, api_output) = self.target.run(
                'cd %s/; /tmp/nodeunit-master/bin/nodeunit %s/%s -t testApiOicResLinksType' % (
                    self.target_rest_api_dir,
                    self.target_rest_api_dir,
                    self.rest_api_js_files['api_oic_res']
                   )
        )
        self.assertEqual(api_status, 0)
        self.assertTrue('OK:' in api_output.strip().splitlines()[-1])


    @classmethod
    def tearDownClass(cls):
        '''
        Clean work.
        Clean all the files and directories that the tests may be used on target.
        '''

        if os.path.exists('%s.tar.gz' % cls.rest_api_dir):
            os.remove('%s.tar.gz' % cls.rest_api_dir)
        if os.path.exists(cls.nodeunit_zip):
            os.remove(cls.nodeunit_zip)

        cls.tc.target.run('rm -f %s.tar.gz' % cls.target_rest_api_dir)
        cls.tc.target.run('rm -fr %s/' % cls.target_rest_api_dir)
        cls.tc.target.run('rm -fr /tmp/nodeunit-master')
        cls.tc.target.run('rm -f /tmp/master.zip')