# Created by pyp2rpm-1.0.1
%global pypi_name taskflow

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Taskflow structured state management library

License:        ASL 2.0
URL:            https://launchpad.net/taskflow
Source0:        http://pypi.io/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-sphinx

Requires:       python-anyjson
Requires:       python-iso8601
Requires:       python-six
Requires:       python-babel
Requires:       python-stevedore
Requires:       python-futures
Requires:       python-networkx-core
Requires:       python-oslo-serialization
Requires:       python-oslo-utils
Requires:       python-jsonschema
Requires:       python-enum34
Requires:       python-debtcollector
Requires:       python-automaton >= 0.5.0
Requires:       python-networkx >= 1.10

%description
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.

%package doc
Summary:          Documentation for Taskflow
Group:            Documentation

%description doc
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.
This package contains the associated documentation.

%prep
%setup -q -n %{pypi_name}-%{upstream_version}
# TODO(apevec) remove once python-networking subpackaging is fixed
sed -i /networkx.drawing/d taskflow/types/graph.py

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%files doc
%doc html

%changelog
