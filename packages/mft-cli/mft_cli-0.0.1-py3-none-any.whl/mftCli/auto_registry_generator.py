import os
import shutil
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
import sys


class AutoRegistryGenerator:

    def __init__(self, project_name, project_location, registry_name, transfer_name):
        self.project_location = project_location
        self.composite_exporter_module_location = f'{project_location}/{project_name}CompositeExporter'
        self.registry_resources_module_location = f'{project_location}/{project_name}RegistryResources'
        self.registry_name = registry_name
        self.transfer_name = transfer_name
        self.default_registry_template_location = os.path.abspath("RegistryTemplate.xml")
        self.temp_dir = os.path.abspath("tmp")
        self.new_registry_file_tmp_location = ''

    def generate_registry_file(self):
        print('Generating registry file...')

        # Set registry file name and copy to temp location
        self.new_registry_file_tmp_location = f'{self.temp_dir}/{self.registry_name}.xml'
        print(f'Generating registry file in temporary location: {self.new_registry_file_tmp_location}')
        shutil.copyfile(self.default_registry_template_location, self.new_registry_file_tmp_location)
        print(f'Successfully generated registry file in temporary location: {self.new_registry_file_tmp_location}')

        # Add transfer name to registry file
        new_registry_file_tree = ET.parse(self.new_registry_file_tmp_location)
        new_registry_file_tree.find('.//transferName').text = self.transfer_name
        new_registry_file_tree.write(self.new_registry_file_tmp_location)

    def add_registry_file_to_project(self):
        print('Adding registry file to project...')

        shutil.move(self.new_registry_file_tmp_location, f"{self.registry_resources_module_location}/{self.registry_name}.xml")

        artifact_item_template = ET.XML(f'''
            <artifact name="{self.registry_name}" groupId="za.co.dearx.resource" version="1.0.0" type="registry/resource" serverRole="EnterpriseIntegrator">
                <item>
                    <file>{self.registry_name}.xml</file>
                    <path>/_system/governance/mftgeneric</path>
                    <mediaType>application/xml</mediaType>
                    <properties/>
                </item>
            </artifact>
        ''')

        artifact_file_location = f"{self.registry_resources_module_location}/artifact.xml"
        artifact_file_tree = ET.parse(artifact_file_location)
        artifact_file_root = artifact_file_tree.getroot()
        artifact_file_root.append(artifact_item_template)
        ET.indent(artifact_file_root, space="\t", level=0)
        artifact_file_tree.write(artifact_file_location)

        composite_pom_properties_template = f'<za.co.dearx.resource_._{self.registry_name}>capp/EnterpriseIntegrator</za.co.dearx.resource_._{self.registry_name}>'

        with open(f"{self.composite_exporter_module_location}/pom.xml", "r") as f:
            contents = f.readlines()

        contents.insert(16, composite_pom_properties_template)

        with open(f"{self.composite_exporter_module_location}/pom.xml", "w") as f:
            contents = "".join(contents)
            f.write(contents)

        composite_pom_dependency_template = ET.XML(f'''
            <dependency>
                <groupId>za.co.dearx.resource</groupId>
                <artifactId>{self.registry_name}</artifactId>
                <version>1.0.0</version>
                <type>zip</type>
            </dependency>
        ''')

        composite_pom_file_location = f"{self.composite_exporter_module_location}/pom.xml"
        composite_pom_file_tree = ET.parse(composite_pom_file_location)
        composite_pom_file_tree.find('.{http://maven.apache.org/POM/4.0.0}dependencies').append(
            composite_pom_dependency_template)
        ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")
        ET.indent(composite_pom_file_tree, space="\t", level=0)
        composite_pom_file_tree.write(composite_pom_file_location, encoding="utf-8", xml_declaration=True)

        print('Successfully added registry file to project...')

    def add_s3_transfer(self, s3_transfer_name, s3_url):
        print(f'Adding S3 transfer to registry file: {self.new_registry_file_tmp_location}')

        if s3_transfer_name.strip() == '':
            print('Error! In order to set up a S3 transfer, a transfer name is required.')
            self.clean_up_temp_directory()
            sys.exit()

        if s3_url.strip() == '':
            print('Error! In order to set up a S3 transfer, a S3 URL is required.')
            self.clean_up_temp_directory()
            sys.exit()

        s3_transfer_template = ET.XML(f'''
            <destination>
                <name>{s3_transfer_name}</name>
                <type>s3</type>
                <url>{s3_url}</url>
            </destination>
        ''')

        tmp_registry_file_tree = ET.parse(self.new_registry_file_tmp_location)
        tmp_registry_file_tree.find('.//destinations').append(s3_transfer_template)
        ET.indent(tmp_registry_file_tree, space="\t", level=0)
        tmp_registry_file_tree.write(self.new_registry_file_tmp_location)
        print(f'Successfully added S3 transfer to registry file: {self.new_registry_file_tmp_location}')


    def add_sftp_transfer(self, sftp_transfer_name, sftp_url):
        print(f'Adding SFTP transfer to registry file: {self.new_registry_file_tmp_location}')

        if sftp_transfer_name.strip() == '':
            print('Error! In order to set up a SFTP transfer, a transfer name is required.')
            self.clean_up_temp_directory()
            sys.exit()

        if sftp_url.strip() == '':
            print('Error! In order to set up a SFTP transfer, a SFTP URL is required.')
            self.clean_up_temp_directory()
            sys.exit()

        sftp_transfer_template = ET.XML(f'''
            <destination>
                <name>{sftp_transfer_name}</name>
                <type>sftp</type>
                <url>{sftp_url}</url>
            </destination>
        ''')

        tmp_registry_file_tree = ET.parse(self.new_registry_file_tmp_location)
        tmp_registry_file_tree.find('.//destinations').append(sftp_transfer_template)
        ET.indent(tmp_registry_file_tree, space="\t", level=0)
        tmp_registry_file_tree.write(self.new_registry_file_tmp_location)

        print(f'Successfully added SFTP transfer to registry file: {self.new_registry_file_tmp_location}')

    def add_sharepoint_transfer(self, sharepoint_transfer_name, sharepoint_url, sharepoint_api_url,
                                sharepoint_tenant_id, sharepoint_client_id, sharepoint_client_secret,
                                sharepoint_redirect_url, sharepoint_folder):

        print(f'Adding Sharepoint transfer to registry file: {self.new_registry_file_tmp_location}')

        if sharepoint_transfer_name.strip() == '':
            print('Error! In order to set up a Sharepoint transfer, a transfer name is required.')
            self.clean_up_temp_directory()
            sys.exit()

        if sharepoint_url.strip() == '':
            print('Error! In order to set up a Sharepoint transfer, a Sharepoint URL is required.')
            self.clean_up_temp_directory()
            sys.exit()

        if sharepoint_api_url.strip() == '':
            print('Error! In order to set up a Sharepoint transfer, a Sharepoint API URL is required.')
            self.clean_up_temp_directory()
            sys.exit()

        if sharepoint_tenant_id.strip() == '':
            print('Error! In order to set up a Sharepoint transfer, a Sharepoint Tenant ID is required.')
            self.clean_up_temp_directory()
            sys.exit()

        if sharepoint_client_id.strip() == '':
            print('Error! In order to set up a Sharepoint transfer, a Sharepoint Client ID is required.')
            self.clean_up_temp_directory()
            sys.exit()

        if sharepoint_client_secret.strip() == '':
            print('Error! In order to set up a Sharepoint transfer, a Sharepoint Client Secret is required.')
            self.clean_up_temp_directory()
            sys.exit()

        if sharepoint_redirect_url.strip() == '':
            print('Error! In order to set up a Sharepoint transfer, a Sharepoint Redirect URL is required.')
            self.clean_up_temp_directory()
            sys.exit()

        if sharepoint_folder.strip() == '':
            print('Error! In order to set up a Sharepoint transfer, a Sharepoint Folder is required.')
            self.clean_up_temp_directory()
            sys.exit()
        resource_url = sharepoint_api_url[8:]
        resource_url = resource_url.split('com/', 1)[0]
        resource_url = f'{resource_url}com'
        sharepoint_resource = f'00000003-0000-0ff1-ce00-000000000000/{resource_url}@{sharepoint_tenant_id}'
        sharepoint_transfer_template = ET.XML(f'''
            <destination>
                <name>{sharepoint_transfer_name}</name>
                <type>sharepoint</type>
                <url>{sharepoint_url}</url>
                <apiUrl>{sharepoint_api_url}</apiUrl>
                <resource>{sharepoint_resource}</resource>
                <clientId>{sharepoint_client_id}</clientId>
                <clientSecret>{sharepoint_client_secret}</clientSecret>
                <tenantId>{sharepoint_tenant_id}</tenantId>
                <redirectUri>{sharepoint_redirect_url}</redirectUri>
                <folderName>{sharepoint_folder}</folderName>
            </destination>
        ''')

        tmp_registry_file_tree = ET.parse(self.new_registry_file_tmp_location)
        tmp_registry_file_tree.find('.//destinations').append(sharepoint_transfer_template)
        ET.indent(tmp_registry_file_tree, space="\t", level=0)
        tmp_registry_file_tree.write(self.new_registry_file_tmp_location)

        print(f'Successfully added Sharepoint transfer to registry file: {self.new_registry_file_tmp_location}')

    def clean_up_temp_directory(self):
        print(f'Cleaning up temp directory: {self.temp_dir}')
        [f.unlink() for f in Path(self.temp_dir).glob("*") if f.is_file()]
        print(f'Successfully cleaned up temp directory: {self.temp_dir}')
