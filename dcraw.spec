Summary:             Tool for decoding raw image data from digital cameras
Name:                dcraw
Version:             9.28.0
Release:             4
License:             GPLv2+
URL:                 http://cybercom.net/~dcoffin/dcraw
Source0:             https://sources.voidlinux.org/dcraw-%{version}/dcraw-%{version}.tar.gz
Patch0:              dcraw-CVE-2018-5801.patch
Patch1:              dcraw-9.21-lcms2-error-reporting.patch
BuildRequires:       gcc gettext libjpeg-devel lcms2-devel
Provides:            bundled(dcraw)
%description
This package contains dcraw, a command line tool to decode raw image data
downloaded from digital cameras.

%prep
%autosetup -n dcraw -p1 -S git

%package             help
Summary:             Documentation for user of dcraw
Requires:            dcraw = %{version}-%{release}

%description         help

%build
gcc %optflags $RPM_LD_FLAGS -lm -ljpeg -llcms2 -DNO_JASPER \
    -DLOCALEDIR="\"%{_datadir}/locale\"" -o dcraw dcraw.c
for catsrc in dcraw_*.po; do
    lang="${catsrc%.po}"
    lang="${lang#dcraw_}"
    msgfmt -o "dcraw_${lang}.mo" "$catsrc"
done

%install
install -Dp -m 0755 dcraw %{buildroot}%{_bindir}/dcraw
for catalog in dcraw_*.mo; do
    lang="${catalog%.mo}"
    lang="${lang#dcraw_}"
    install -d -m 0755 "%{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES"
    install -m 0644 "$catalog" "%{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES/dcraw.mo"
done
install -d -m 0755 %{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1
install -m 0644 dcraw.1 %{buildroot}%{_mandir}/man1/dcraw.1
rm -f %{name}-man-files
touch %{name}-man-files
for manpage in dcraw_*.1; do
    lang="${manpage%.1}"
    lang="${lang#dcraw_}"
    install -d -m 0755 "%{buildroot}%{_mandir}/${lang}/man1"
    install -m 0644 "${manpage}" "%{buildroot}%{_mandir}/${lang}/man1/dcraw.1"
    echo "%%lang($lang) %%{_mandir}/${lang}/man1/*" >> %{name}-man-files
done
%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/dcraw

%files help  -f %{name}-man-files
%{_mandir}/man1/*

%changelog
* Fri Sep 11 2020 leiju <leiju4@huawei.com> - 9.28.0-4
- Delete BuildRequires jasper-devel

* Tue Apr 21 2020 Jeffery.Gao <gaojianxing@huawei.com> - 9.28.0-3
- Package init
