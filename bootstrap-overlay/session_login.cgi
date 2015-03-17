#!/usr/bin/perl
# session_login.cgi
# Display the login form used in session login mode

BEGIN { push(@INC, ".."); };
use WebminCore;
$name = (&get_product_name() eq 'usermin') ? 'Usermin' : 'Webmin';
$pragma_no_cache = 1;
&ReadParse();
&init_config();

%text = &load_language($current_theme);
%gaccess = &get_module_acl(undef, "");
&get_miniserv_config(\%miniserv);
$title = &get_html_framed_title();
$sec = uc($ENV{'HTTPS'}) eq 'ON' ? "; secure" : "";
$sidname = $miniserv{'sidname'} || "sid";
print "Set-Cookie: banner=0; path=/$sec\r\n" if ($gconfig{'loginbanner'});
print "Set-Cookie: $sidname=x; path=/$sec\r\n" if ($in{'logout'});
print "Set-Cookie: testing=1; path=/$sec\r\n";
$charset = &get_charset();
&PrintHeader($charset);
if ($gconfig{'realname'}) {
	$host = &get_display_hostname();
}
else {
	$host = $ENV{'HTTP_HOST'};
	$host =~ s/:\d+//g;
	$host = &html_escape($host);
}
$tag = $gconfig{'noremember'} ? 'autocomplete="off"' : '';
# Look up (there's something wrong with cookies or maybe i think)
print '<!DOCTYPE HTML>' , "\n";
print '<html>' , "\n";
print '<head>' , "\n";
print '<title>' , $title , '</title>' , "\n";
print '<meta charset="utf-8">' , "\n";
print '<meta name="viewport" content="width=device-width, initial-scale=1.0">' . "\n";
print '<link href="' . $gconfig{'webprefix'} . 'unauthenticated/css/foundation.css" rel="stylesheet" type="text/css">' , "\n";
print '<link href="' . $gconfig{'webprefix'} . 'unauthenticated/css/responsivebacula.css" rel="stylesheet" type="text/css">' , "\n";
print '<link href="' . $gconfig{'webprefix'} . 'unauthenticated/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">' , "\n";

print '<script src="' . $gconfig{'webprefix'} . 'unauthenticated/js/vendor/modernizr.js"></script>' , "\n";
print '</head>' , "\n";
print '<body>' . "\n";

print '<!-- Top bar/Nav e Side bar -->' , "\n";
print '<div class="off-canvas-wrap fixed" data-offcanvas>' , "\n";
print '<div class="inner-wrap">' , "\n";
print '<nav class="top-bar tab-bar">' , "\n";
      
print '<div class="large-4 medium-4 small-4 columns ">' , "\n";
print '<ul class="title-area">' , "\n";
print '<li class="name row"><h1><a href="#">' , "\n";
print '<span class="bacula-title">Bacula</span>' , "\n";
print '<span class="backups-title"> Backups</span></a></h1>' , "\n";
print '</li>' , "\n";
print '</ul>' , "\n";
print '</div>' , "\n";
  
print '<!-- Logo -->' , "\n";
print '<div class="large-4 columns hide-for-medium hide-for-small central-logo">' , "\n";
print '<img class="bacula_logo" src="' . $gconfig{'webprefix'} . 'unauthenticated/img/logos/bacula_logo.png" alt="Bacula Backups">' , "\n";
print '</div>' , "\n";


  
print '<section class="right-small sidebar">' , "\n";

print '</section>' , "\n";
print '</nav>' , "\n";
 
 
print '<!-- ##### corpo #####-->' , "\n";


print '<!--##############################################################################################################-->' , "\n";
print '<form method="post" action="' . $gconfig{'webprefix'} . '/session_login.cgi" role="form">' . "\n";
print '<section class="main-section">' , "\n";
print '<!--##############################################################################################################-->' , "\n";
print '<!--corpo-->' , "\n";

print '<section id="login">' , "\n";
print '<div class="row">   ' , "\n";
print '<div class="large-4 large-offset-4 medium-4 medium-offset-4 small-10 small-offset-1 text-center login">' , "\n";
print '<label>username' , "\n";
#print '<input type="text" placeholder="">' , "\n";
print '<input type="text" placeholder="Username" name="user" ' . $tag . '>' . "\n";
print '</label>' , "\n";
print '<label>password' , "\n";
#print '<input type="password" placeholder="">' , "\n";
print '<input type="password" placeholder="Password" name="pass" ' . $tag . '>' . "\n";
print '</label>' , "\n";
print '</div>' , "\n";
	    
print '<div id="remember" class="large-6 large-offset-3 medium-6 medium-offset-3 small-12 text-center">' , "\n";
print '<input class="checkedBox" id="checkbox1" type="checkbox"><label for="checkbox1"><span class="remember">remember me</span></label>' , "\n";
print '</div>' , "\n";
	  
if (defined($in{'failed'})) {
	print '<div class="col-xs-12 col-sm-fix">' . "\n";
	print '<div class="message-container">' . "\n";
	if ($in{'twofactor_msg'}) {
		print '<div class="alert alert-danger">' . "\n";
		print '<strong><i class ="fa fa-bolt"></i> Danger!</strong><br />' . &text('session_twofailed', &html_escape($in{'twofactor_msg'})) . "\n";
		print '</div>' . "\n";
	} else {
		print '<div class="alert alert-danger">' . "\n";
		print '<strong><i class ="fa fa-bolt"></i> Danger!</strong><br />' . "\n";
		print $text{'session_failed'} . "\n";
		print '</div>' . "\n";
	}
	print '</div>' . "\n";
	print '</div>' . "\n";
}
elsif ($in{'logout'}) {
	print '<div class="col-xs-12 col-sm-fix">' . "\n";
	print '<div class="message-container">' . "\n";
	print '<div class="alert alert-success">' . "\n";
	print '<strong><i class ="fa fa-check"></i> Success!</strong><br />' . "\n";
	print $text{'session_logout'} . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
}
elsif ($in{'timed_out'}) {
	print '<div class="col-xs-12 col-sm-fix">' . "\n";
	print '<div class="message-container">' . "\n";
	print '<div class="alert alert-warning">' . "\n";
	print '<strong><i class ="fa fa fa-exclamation-triangle"></i> Warning!</strong><br />' . "\n";
	print &text('session_timed_out', int($in{'timed_out'}/60)) . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
}
print '<div class="row collapse" id="login_buttons">' , "\n";
print '<div class="large-2 large-offset-4 medium-6 hide-for-small columns collapse">' , "\n";
print '<a href="#" class="button secondary expand">CLEAR</a>' , "\n";
print '</div>' , "\n";
	  
print '<div class="large-2 medium-6 small-12 columns left">' , "\n";
#print '<a href="index.html" class="button success expand">ENTER</a>' , "\n";
print '<button type="submit" class="button success expand">ENTER</button>' . "\n";
print '</div>' , "\n";
print '</div>' , "\n";
print '</div>' , "\n";
print '</form>' . "\n";
print '</section>' , "\n";
print '</section>' , "\n";
    
print '<footer>' , "\n";
print '<div class="large-12 medium-12 small-12">' , "\n";
print '<div class="large-12 medium-12 small-12 columns">' , "\n";
print '<a href="http://www.versaointegral.pt"><img class="vi_logo" src="' . $gconfig{'webprefix'} . 'unauthenticated/img/logos/vi_logo.png" alt="Versao Integral"/></a>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '</div>' , "\n";
print '</footer>  ' , "\n";
print '</div>' , "\n";

print '<!--##############################################################################################################-->' , "\n";

print '<script src="' . $gconfig{'webprefix'} . 'unauthenticated/js/vendor/jquery.js"></script>' , "\n";
print '<script src="' . $gconfig{'webprefix'} . 'unauthenticated/js/foundation.min.js"></script>' , "\n";
print '<script>' , "\n";
print '$(document).foundation();' , "\n";
print '</script>' , "\n";
print '<script>' , "\n";
print <<'ENDHTML';
      $(document).ready(function(){
	$('a[href*=#]').click(function() {
	  if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'')
	  && location.hostname == this.hostname) {
	    var $target = $(this.hash);
	    $target = $target.length && $target
	    || $('[name=' + this.hash.slice(1) +']');
	    if ($target.length) {
	      var targetOffset = $target.offset().top;
	      $('html,body')
	      .animate({scrollTop: targetOffset}, 800);
	     return false;
	    }
	  }
	});
      });
ENDHTML
print '</script>' , "\n";


&footer();