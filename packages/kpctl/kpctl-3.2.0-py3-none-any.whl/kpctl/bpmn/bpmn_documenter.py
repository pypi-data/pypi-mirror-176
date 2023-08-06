###############################################################################
# Copyright 2015-2022 Tim Stephenson and contributors
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License.  You may obtain a copy
#  of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations under
#  the License.
#
# Command line client for managing process application lifecycle.
#
###############################################################################
from cairosvg import svg2png
import lxml.etree as ET
import os
import requests
from kpctl.constants import NS

from kpctl.xml_support import write_pretty_xml

XSLT_PROC_RENDERER = 'http://modeler.knowprocess.com/xslt/bpmn2svg.xslt'

class BpmDocumenter():
    def __init__(self, options):
        self.options = options

    def document(self, input_):
        if self.options.verbose:
            print('generating documentation...')

        if input_.endswith('.bpmn'):
            self.generate_proc_image(input_)
        elif input_.endswith('.form'):
            self.generate_form_image(input_)
        else:
            for root, dirs, files in os.walk(input_):
                for file in files:
                    if file.endswith('.bpmn'):
                        self.generate_proc_image(root+'/'+file)
                    elif file.endswith('.form'):
                        self.generate_form_image(root+'/'+file)

        if self.options.verbose:
            print('...done')

    def generate_form_image(self, form_file):
        if self.options.verbose:
            print('  generating image for ...'+form_file)
            print('  ...not yet implemented...')

    def generate_proc_image(self, bpmn_file):
        if self.options.verbose:
            print('  generating image for ...'+bpmn_file)

        dom = ET.parse(bpmn_file)
        res = requests.get(XSLT_PROC_RENDERER)
        xslt = ET.fromstring(res.content)
        transform = ET.XSLT(xslt)
        diags = dom.findall('//bpmndi:BPMNDiagram', NS)
        for count, diag in enumerate(diags):
            if self.options.verbose:
                print('found diag {}'.format(diag.get('id')))
            newdom = transform(dom, diagramId=ET.XSLT.strparam(diag.get('id')))
            #newdom = transform(dom)
            write_pretty_xml(bpmn_file+'.'+str(count+1)+'.svg', newdom)
            try:
                svg2png(bytestring=ET.tostring(newdom, encoding='unicode'), write_to=bpmn_file+'.png')
            except Exception as e:
                print('  ... unable to create png of the process: {}'.format(e))

            # now generate language variants
            try:
                langs = dom.findall('//i18n:translation[@xml:lang]', NS)
                langs = set(map(lambda x : x.get('{http://www.w3.org/XML/1998/namespace}lang'), langs))
                if (len(langs)>0):
                    if self.options.verbose:
                        print('  detected the following languages: "{}"'.format(langs))
                    for l in langs:
                        if self.options.verbose:
                            print("    generating localised '%s' image ..." % l)
                        newdom = transform(dom, diagramId=ET.XSLT.strparam(diag.get('id')),
                                           lang=ET.XSLT.strparam(l))
                        write_pretty_xml(bpmn_file+'.'+str(count+1)+'.'+l+'.svg', newdom)
                        svg2png(bytestring=ET.tostring(newdom, encoding='unicode'), write_to=bpmn_file+'.'+l+'.png')
                else:
                    if self.options.verbose:
                        print('  ... no translations found to document')
            except KeyError as e:
                if self.options.verbose:
                    print('  ... unable to render translations: {} '.format(e))
