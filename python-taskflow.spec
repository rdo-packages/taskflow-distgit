# Created by pyp2rpm-1.0.1
%global pypi_name taskflow

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# see https://fedoraproject.org/wiki/Packaging:Python#Macros
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           python-%{pypi_name}
Version:        1.18.0
Release:        1%{?dist}
Summary:        Taskflow structured state management library

License:        ASL 2.0
URL:            https://launchpad.net/taskflow
Source0:        http://pypi.python.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-oslo-sphinx
%if 0%{?rhel} == 6
BuildRequires:  python-sphinx10
%else
BuildRequires:  python-sphinx
%endif

Requires:       python-anyjson
Requires:       python-automaton >= 0.2.0
Requires:       python-babel
Requires:       python-cachetools >= 1.0.0
Requires:       python-contextlib2 >= 0.4.0
Requires:       python-debtcollector >= 0.3.0
Requires:       python-enum34
Requires:       python-fasteners >= 0.7
Requires:       python-futures >= 3.0
Requires:       python-futurist >= 0.1.2
Requires:       python-iso8601
Requires:       python-jsonschema
Requires:       python-monotonic >= 0.1
Requires:       python-networkx-core
Requires:       python-oslo-serialization >= 1.4.0
Requires:       python-oslo-utils >= 1.9.0
Requires:       python-pbr
Requires:       python-six >= 1.9.0
Requires:       python-stevedore >= 1.5.0

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
%if 0%{?rhel} == 6
sphinx-1.0-build doc/source html
%else
sphinx-build doc/source html
%endif
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%files
%doc README.rst LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%files doc
%doc html

%changelog
* Tue Aug 18 2015 Alan Pevec <alan.pevec@redhat.com> 1.18.0-1
- Update to upstream 1.18.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 31 2015 Haikel Guemar <hguemar@fedoraproject.org> 0.7.1-1
- Update to upstream 0.7.1

* Sat Jan 17 2015 Haikel Guemar <hguemar@fedoraproject.org> 0.5.0-1
- Update to upstream 0.5.0
- Drop remove runtime dep on pbr patch
- Add new requirements

* Thu Aug 28 2014 Pádraig Brady <pbrady@redhat.com> - 0.3.21-1
- Latest upstream

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Pádraig Brady <pbrady@redhat.com> - 0.1.2-6
- Remove dependence on pbr

* Sun Mar 16 2014 Padraig Brady <P@draigBrady.com> - 0.1.2-5
- Reduce dependency to python-networkx-core subpackage

* Wed Jan 29 2014 Padraig Brady <P@draigBrady.com> - 0.1.2-4
- Initial package.
