line1=Opciones configurables,11
show_list=Mostrar servidores virtuales como,1,0-Iconos,1-Lista
show_order=Ordenar servidores virtuales por,1,0-Orden en archivos de configuraci&#243;n,1-Nombre de servidor,2-Direcci&#243;n IP
max_servers=M&#225;ximo n&#250;mero de servidores a mostrar,0,5
virt_file=Archivo o directorio al que a&#241;adir servidores virtuales,3,httpd.conf
virt_name=Esquema de nombre de archivo para servidores virtuales,3,Por defecto ($DOM.conf)
test_config=&#191;Testear archivo de configuraci&#243;n antes de aplicar los cambios?,1,1-S&#237;,0-No
test_manual=&#191;Testear archivo de configuraci&#243;n tras cambios manuales?,1,1-S&#237;,0-No
test_always=&#191;Testear el archivo de configuraci&#243;n tras otros cambios?,1,1-S&#237;,0-No
test_apachectl=Testear configuraci&#243;n con el comando,1,1-<tt>apachectl configtest</tt>,0-<tt>httpd</tt> con opciones <tt>-D</tt>
show_names=Mostrar nombres de directiva de Apache,1,1-S&#237;,0-No
apache_docbase=Directorio base para la documentaci&#243;n Apache,3,Web de Apache
line2=Configuraci&#243;n del sistema,11
httpd_dir=Directorio ra&#237;z de servidor Apache,0
httpd_path=Trayectoria a ejecutable httpd,0
httpd_version=Versi&#243;n de Apache,3,Funcionar autom&#225;ticamente
apachectl_path=Trayectoria a comando apachectl,3,Ninguna
start_cmd=Comando para arrancar apache,3,Utilizar apachectl o comenzar manualmente
stop_cmd=Comando para parar apache,3,Usar apachectl o matar proceso
apply_cmd=Comando para aplicar configuraci&#243;n,3,Utilizar apachectl o se&#241;al HUP
graceful_cmd=Comando para releer configuraci&#243;n,3,El mismo que el comando aplicar
httpd_conf=Trayectoria a httpd.conf,3,Autom&#225;tica
srm_conf=Trayectoria a srm.conf,3,Autom&#225;tica
access_conf=Trayectoria a access.conf,3,Autom&#225;tica
mime_types=Trayectoria a mime.types,3,Autom&#225;tica
pid_file=Trayectoria al archivo PID de Apache,3,Averiguarlo autom&#225;ticamente
