line1=Configuraci&#243;n del servidor,11
mail_system=Servidor de correo a configurar,4,1-Sendmail,0-Postfix,2-Qmail,4-Qmail+LDAP,5-Qmail+VPOPMail,3-Detectar autom&#225;ticamente
generics=Tambi&#233;n actualizar direcciones salientes para cuentas de correo?,1,1-Si,0-No
quotas=Configuraci&#243;n de quota para el dominio y usuarios de correo?,1,1-Si (si se encuentra habilitado),0-No
iface=Interface de red para direcciones virtuales,3,Detectar autom&#225;ticamente
iface_base=Base number for virtual interfaces,3,Automatic
defip=Direcci&#243;n IP por defecto del servidor virtual,3,La de la placa de red
dns_ip=Direcci&#243;n IP por defecto para los registros de DNS,3,La misma IP que la del servidor virtual
dns_check=Chequear el archivo  resolv.conf para este sistema?,1,1-Si,0-No
disable=Opciones a desactivar al deshabilitar,13,Usuario de Administraci&#243;n-unix (bloquear cuenta),mail-Mail (no aceptar mas mails para el dominio),web-Website (reemplazar el sitio con una p&#225;gina de error),dns-DNS (dejar de resolver el dominio),mysql-MySQL (deshabilitar logueo de usuario de MySQL),postgres-PostgreSQL (deshabilitar logueo de usuario de PostgreSQL),ftp-ProFTPD (rechazar acceso)
delete_indom=Eliminar en el Apache todos los hosts virtuales del dominio en el borrado?,1,1-Si,0-No
ldap=Guardar usuarios y grupos,1,1-En base de datos LDAP,0-En archivos locales
ldap_mail=A&#241;adir atribuciones de correo para usuarios de LDAP?,1,1-Si utilizando solamente atributos<tt>mail</tt> ,2-Si utilizando <tt>mail</tt> y <tt>mailAlternateAddress</tt>,0-No
compression=Formato de compresi&#243;n del Backup,1,0-gzip,1-bzip2,2-Ninguno (solo tar)
maillog_period=Cantidad de d&#237;as para mantener los logs de mail procesados,3,Para siempre
allow_upper=Forzar el uso de min&#250;sculas en los nombres de usuario de las casillas de correo?,1,0-Si,1-No
mysql_replicas=Servidores adicionales de MySQL para crear usuarios,3,Solo este sistema
delete_virts=Eliminar todos los aliases de correo al deshabilitar el correo?,1,1-Si,0-No
preload_mode=Precargar las librer&#237;as del Virtualmin al arrancar?,1,2-Todas las librer&#237;as,1-Solo core,0-No
line1.4=Configuraci&#243;n de la interfaz del usuario,11
display_max=N&#250;mero m&#225;ximo de dominios para mostrar,3,Ilimitado
name_max=Largo maximo de nombre de dominio a mostrar,0,5
show_features=Mostrar las caracter&#237;sticas del servidor en la p&#225;gina principal?,1,1-Si,0-No
show_quotas=Mostrar el espacio utilizado en disco en la p&#225;gina principal?,1,1-Si,0-No
show_mailsize=Mostrar la capacidad de la cuenta de correo en la lista de usuarios?,1,1-Si,0-No
show_sysinfo=Mostrar informaci&#243;n del sistema en la p&#225;gina principal?,1,1-Si,0-No,2-Solo para el administrador principal,3-Solo para el administrador principal y resellers
template_auto=Permitir editar las opciones de la plantilla al crear el servidor?,1,0-Si,1-No
domains_sort=Ordenar los servidores virtuales por,1,usuario-Due&#241;o,dom-Nombre del Dominio,Due&#241;o-Descripci&#243;n
show_ugroup=Permitir seleccionar grupos diferentes para administradores del servidor?,1,1-Si,0-No
theme_image=Direcci&#243;n web (URL) del logo de la empresa,3,Ninguna o por defecto,50
theme_link=Direcci&#243;n de Internet a donde desea que vaya al cliquear el logo,3,Ninguna,50
line1.5=Permisos del administrador del servidor,11
edit_afiles=Can edit alias include and reply files?,1,1-Yes,0-No
edit_homes=Puede seleccionar el directorio principal para los usuarios?,1,1-Si,0-No
edit_ftp=Puede crear usuarios de FTP?,1,1-Si,0-No
edit_quota=Puede setear quotas de correo?,1,1-Si,0-No
show_pass=Puedo ver contrase&#241;as de correo y del servidor virtual?,1,1-Si,0-No
batch_create=Puede crear m&#250;ltiples servidores desde un archivo?,1,1-Si,0-No
alias_types=Tipos de aliases permitidos,13,1-Direcci&#243;n,2-Direcciones en el archivo,3-Archivo,4-Programa,5-Contestador autom&#225;tico,6-Filtro,7-Otra casilla de correo del usuario,8-La misma casilla de correo en el dominio,9-Rebote,10-Casilla de correo del usuario,11-Borrar,12-Archivo del contestador autom&#225;tico
post_check=Actualizar todos los usuarios del Webmin luego de cambios en la configuraci&#243;n?,1,1-Si,0-No
leave_acl=Siempre actualizar los m&#243;dulos ACLs de Webmin?,1,0-Si,1-No
webmin_modules=M&#243;dulos adicionales de Webmin para administradores del servidor,15,modules,webmin_modules
webmin_theme=Plantilla de Webmin para administradores de servidor,15,theme,webmin_theme
show_tabs=Categorizar los m&#243;dulos del Webmin en el men&#250; principal?,1,1-Si,0-No
domains_group=Agregar todas las administraciones del servidor al grupo Unix group,3,Ninguna
line2=Defaults para nuevos dominos,11
home_base=Home directory base,3,From Users and Groups module
home_format=Subcarpeta Home,10,-Autom&#225;tico,Desde plantilla (puede utilizar $USER y $DOM)
append=Incluir el nombre del dominio en los nombres de usuario?,1,1-Siempre,0-Solo para evitar duplicaciones
longname=Estilo del nombre de dominio en el nombre de usuario,1,1-Nombre de dominio completo,0-Nombre de usuario o primera parte del dominio ,2-Primera parte del dominio
groupsame=Forzar el nombre del grupo para que sea siempre el mismo que el nombre de usuario?,1,1-Si,0-No
localgroup=Grupo primario para usuarios locales,3,No mostrar usuarios locales
mail_skel=Carpeta de archivos inicial para usuarios de correo,3,Ninguna
proxy_pass=Permitir la creaci&#243;n de sitios que solamente redireccionan?,1,1-Si&#44; usando proxy2-Si&#44; utilizando redireccionamiento por frames,0-No
homes_dir=Subdirectory for mailbox user home directories,0,20
passwd_mode=Tipo de campo de contrase&#241;a,1,1-Contrase&#241;a generada al azar,0-Ingresar la contrase&#241;a una &#250;nica vez,2-Ingresar la contrase&#241;a dos veces
passwd_length=Largo de la contrase&#241;a generada al azar,3,Default (15 caracteres),5
webalizer_nocron=Configurar en cron de Webalizer para cada servidor virtual?,1,0-Si,1-No
limitnoalias=Include alias servers in limits?,1,0-Yes,1-No
allow_subdoms=Se permite la creaci&#243;n de subdominios?,1,1-Si,0-No,-Decidir autom&#225;ticamente
denied_domains=Expresiones regulares para dominios deshabilitados,0
line2.1=Configuraci&#243;n SSL,11
key_size=Tama&#241;ano del key SSL por defecto,3,Webmin default (512 bits),6,,bits
key_tmpl=Plantilla para ruta de clave privada (private key),3,Default (<tt>~/ssl.key</tt>)
cert_tmpl=Plantilla para la ruta del certificado,3,Default (<tt>~/ssl.cert</tt>)
ca_tmpl=Template for CA certificate path,3,Default (<tt>~/ssl.ca</tt>)
line6.5=Configuraci&#243;n de Reseller,11
reseller_theme=Plantilla para nuevo reseller,15,theme,reseller_theme
reseller_modules=M&#243;dulos adicionales para resellers,15,modules,reseller_modules
line4=Acciones al crear servidores y usuarios,11
from_addr=De: Direcci&#243;n para correo enviada por Virtualmin,3,Default
pre_command=Comando a ejecutar antes de realizar cambios en un servidor,0
post_command=Comando a ejecutar luego de realizar cambios en un servidor,0
alias_pre_command=Comando para ejecutar antes de hacer cambios a un alias,0
alias_post_command=Comando para ejecutar luego de hacer cambios a un alias,0
other_users=Notificar a otros m&#243;dulos al actualizar usuarios de administraci&#243;n de servidor Unix?,1,1-Si,0-No
other_doms=Notificar a otros m&#243;dulos al actualizar usuarios de correo Unix?,1,1-Si,0-No
check_apache=Chequear la configuraci&#243;n del Apache antes de aplicar cambios?,1,1-Si,0-No
line4.5=Opciones de Qmail+LDAP,11
ldap_host=Servidor LDAP,0
ldap_port=Puerto LDAP,3,Default
ldap_login=Logueo para el servidor LDAP,0
ldap_pass=Contrase&#241;a para el servidor LDAP,0
ldap_base=Base for mail users,0
ldap_unix=Los usuarios de Qmail LDAP son tambi&#233;n usuario de Unix?,1,1-Si,0-No
ldap_mailstore=Guardado de mail para usuarios,0
ldap_classes=Object classes adicionales para usuarios LDAP ,0
ldap_aclasses=Object classes adicionales para aliases LDAP ,0
ldap_props=Atributos adicionales para usuarios LDAP,9,40,3,\t
line4.6=Opciones de VPOPMail,11
vpopmail_dir=Directorio base para VPOPMail,0
vpopmail_user=Usuario VPOPMail,5
vpopmail_group=Grupo VPOPMail,6
vpopmail_auto=Ruta a el programa de autorresponder,3,No instalado
line4.7=Opciones de filtrado de Spam,11
spam_delivery=Entrega de Spam por defecto,10,-Entrega normal,/dev/null-Delete,$HOME/mail/spam-Spam mbox folder,$HOME/Maildir/.spam/-Spam Maildir folder,Otro archivo o direcci&#243;n de correo
default_procmail=Permitir a usuarios de cuentas de correo configurar el procmail?,1,0-Si,1-No
clam_delivery=Entrega de visrus por defecto,10,/dev/null-Delete,$HOME/mail/virus-Virus mbox folder,$HOME/Maildir/.virus/-Virus Carpeta Maildir,otro archivo o direcci&#243;n de correo
spam_white=Opci&#243;n de lista blanca de spam por defecto,1,1-Habilitado,0-Deshabilitado
line4.8=Comandos de Quota,11
quota_commands=Utilizar comandos externos para obtener y setear quotas?,1,1-Si,0-No
quota_set_user_command=Comando para setear quotas de usuario,3,Utilizar programas Standard
quota_set_group_command=Comando para setear quotas de grupo,3,Utilizar programas Standard
quota_list_users_command=Comando para listar quotas de usuario,3,Utilizar programas Standard
quota_list_groups_command=Comando para listar quotas de grupo,3,Utilizar programas Standard
quota_get_user_command=Comando para obtener la quota de un usuario,3,Utilizar programas Standard
quota_get_group_command=Comando para obtener la quota de un grupo,3,Utilizar programas Standard
line5=M&#243;dulos del Webmin disponibles para los administradores del servidor,11
avail_dns=Servidor de DNS BIND (para los DNS del dominio),1,1-Si,0-No
avail_mail=Email Virtual (para casillas de correo y aliases),1,1-Si,0-No
avail_web=Servidor Web Apache (para host virtual),1,1-Si,0-No
avail_webalizer=Estad&#237;sticas Webalizer (para estad&#237;sticas del sitio),1,1-Si,0-No
avail_mysql=Servidor de base de datos MySQL (para base de datos),1,1-Si,0-No
avail_postgres=Servidor de base de datos PostgreSQL (para base de datos),1,1-Si,0-No
avail_spam=Filtro de correo SpamAssassin (para archivo de configuraci&#243;n de los dominios),1,1-Si,0-No
line3=M&#243;dulos extra disponibles para los administradores del servidor,11
avail_file=Editor de Archivos (solo para el directorio home),1,1-Si,0-No
avail_passwd=Cambiar contrase&#241;a,1,2-contrase&#241;a de usuario y de correo,1-Contrase&#241;a de usuario,0-No
avail_proc=Procesos en curso (solo procesos del usuario),1,2-Ver procesos propios,1-Ver todos los procesos,0-No
avail_cron=Tareas programadas de Cron (tareas de cron del usuario),1,1-Si,0-No
avail_at=Comandos programados (comandos del usuario),1,1-Si,0-No
avail_telnet=SSH/Telnet Login,1,1-Si,0-No
avail_updown=Subida y Bajada (como usuario),1,1-Si,0-No,2-Solamente Subida
avail_change-user=Cambiar idioma y tema,1,1-Si,0-No
avail_mailboxes=Leer correo del usuario (casillas de correo de los usuarios),1,1-Si,0-No
avail_custom=Comandos a medida,1,1-Si,0-No
avail_shell=L&#237;nea de comando (ejecuta comandos como admin),1,1-Si,0-No
avail_webminlog=Log de acciones del Webmin (ver las propias acciones),1,1-Si,0-No
avail_syslog=Logs del sistema (Para ver los logs del Apache y del FTP),1,1-Si,0-No
avail_phpini=Configuraci&#243;n del PHP (para el archivo php.ini del dominio),1,1-Si,0-No
