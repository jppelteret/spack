##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import subprocess


class JupyterNotebook(Package):
    """A web application that allows you to create and share documents that contain live code, 
    equations, visualizations and explanatory text. Uses include: data cleaning and 
    transformation, numerical simulation, statistical modeling, machine learning and much more."""
    
    homepage = "http://jupyter.org/"
    url      = "https://github.com/jupyter/notebook/archive/4.2.1.tar.gz"

    version('4.2.1', '2b222d9edebbf095ba8125162a5d6530edeef80a')
    
    variant('ipython',     default=True, description='Enable ipython support')
    #variant('ipywidgets',  default=False,  description='Enable with support')
    #variant('ipyparallel', default=False,  description='Enable with support')

    # http://simnotes.github.io/blog/installing-jupyter-on-hdp-2.3.2/
    
    def cmd_exists(cmd):
      try:
          subprocess.check_output(["which", cmd])
          return True
      except subprocess.CalledProcessError as ex:
          return False
    
    depends_on('python',        type='build') # 2.7 or >=3.3
    depends_on('py-setuptools', type='build')
    if (cmd_exists("bower") == False & cmd_exists("npm") == False & cmd_exists("node") == False):
        depends_on('node-js',   type='build')
        depends_on('npm',       type='build')
    depends_on('py-numpy')
    depends_on('py-scipy')
    depends_on('py-pandas')
    depends_on('py-scikit-learn')
    depends_on('py-tornado')
    depends_on('py-zmq')
    depends_on('py-pygments')
    depends_on('py-matplotlib')
    depends_on('py-jinja2')
    depends_on('py-jsonschema')
    depends_on('py-ipython',      when="+ipython")
    #depends_on('py-ipywidgets',   when="+ipywidgets")
    #depends_on('py-ipyparallel',  when="+ipyparallel")
    
    # Unfortunately either bower (preferred) or npm must be used to install
    # the remaining dependencies. If bower is in path, this is automatically
    # invoked from within the setup script. But we will just use npm to do
    # it manually, just in case Bower is not present on the system...
    def install(self, spec, prefix):
      python('setup.py', 'install', '--prefix={0}'.format(prefix))
