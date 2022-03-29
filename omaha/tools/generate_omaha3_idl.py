#!/usr/bin/python2.4
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================

"""Generates IDL file Omaha3 internfaces."""

import commands
import getopt
import os
import sys


def _GetStatusOutput(cmd):
  """Return (status, output) of executing cmd in a shell."""
  if os.name == "nt":
    pipe = os.popen(cmd + " 2>&1", "r")
    text = pipe.read()
    sts = pipe.close()
    if sts is None: sts = 0
    if text[-1:] == "\n": text = text[:-1]
    return sts, text
  else:
    return commands.getstatusoutput(cmd)


def _GenerateGuid():
  (status, guid) = _GetStatusOutput("uuidgen.exe /c")
  if status != 0:
    raise SystemError("Failed to get GUID: %s" % guid)
  return guid


def _GenerateIDLText(idl_template):
  guid_placehold_marker = "___AUTO_GENERATED_GUID___"
  while guid_placehold_marker in idl_template:
    idl_template = idl_template.replace(guid_placehold_marker,
                                        _GenerateGuid(),
                                        1)
  return idl_template


def _GenerateIDLFile(idl_template_filename, idl_output_filename):
  f_in = open(idl_template_filename, "r")
  idl_template = f_in.read()
  f_in.close()

  idl_output = _GenerateIDLText(idl_template)

  f_out = open(idl_output_filename, "w")
  f_out.write("// *** AUTOGENERATED FILE. DO NOT HAND-EDIT ***\n\n")
  f_out.write(idl_output)
  f_out.close()


def _Usage():
  """Prints out script usage information."""
  print """
generate_omaha3_idl.py: Write out the given IDL file.

Usage:
  generate_omaha3_idl.py [--help
                          | --idl_template_file filename
                            --idl_output_file filename]

Options:
  --help                        Show this information.
  --idl_output_file filename    Path/name of output IDL filename.
  --idl_template_file filename  Path/name of input IDL template.
"""


def _Main():
  """Generates IDL file."""
  # use getopt to parse the option and argument list; this may raise, but
  # don't catch it
  argument_list = ["help", "idl_template_file=", "idl_output_file="]
  (opts, unused_args) = getopt.getopt(sys.argv[1:], "", argument_list)
  if not opts or ("--help", "") in opts:
    _Usage()
    sys.exit()

  idl_template_filename = ""
  idl_output_filename = ""

  for (o, v) in opts:
    if o == "--idl_template_file":
      idl_template_filename = v
    if o == "--idl_output_file":
      idl_output_filename = v

  # make sure we have work to do
  if not idl_template_filename:
    raise StandardError("no idl_template_filename specified")
  if not idl_output_filename:
    raise StandardError("no idl_output_filename specified")

  _GenerateIDLFile(idl_template_filename, idl_output_filename)
  sys.exit()


if __name__ == "__main__":
  _Main()

