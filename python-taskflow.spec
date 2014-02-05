# Created by pyp2rpm-1.0.1
%global pypi_name taskflow

Name:           python-%{pypi_name}
Version:        0.1.2
Release:        4%{?dist}
Summary:        Taskflow structured state management library

License:        ASL 2.0
URL:            https://launchpad.net/taskflow
Source0:        http://pypi.python.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-sphinx

Requires:       python-anyjson
Requires:       python-iso8601
Requires:       python-six
Requires:       python-babel
Requires:       python-stevedore
Requires:       python-futures
Requires:       python-networkx

%description
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.

%package doc
Summary:          Documentation for OpenStack Compute
Group:            Documentation

%description doc
A library to do [jobs, tasks, flows] in a HA manner using
different backends to be used with OpenStack projects.
This package contains the associated documentation.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

# generate html docs
sphinx-build doc html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --skip-build --root %{buildroot}


%files
%doc README.md LICENSE
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files doc
%doc html

%changelog
* Wed Jan 29 2014 Padraig Brady <P@draigBrady.com> - 0.1.2-4
- Initial package.
