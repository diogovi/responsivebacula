
print '<head>' , "\n";
print '<meta charset="utf-8" />' , "\n";
print '<meta name="viewport" content="width=device-width, initial-scale=1.0" />' , "\n";
print '<title>Responsive Bacula</title>' , "\n";
print '<link rel="stylesheet" href="css/foundation.css" />' , "\n";
print '<link rel="stylesheet" href="css/responsivebacula.css" />' , "\n";
print '<link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">' , "\n";
print '<script src="js/vendor/modernizr.js"></script>' , "\n";
print '</head>' , "\n";
print '<body>' , "\n";

print '<!-- Top bar/Nav e Side bar -->' , "\n";
print '<div class="off-canvas-wrap fixed" data-offcanvas>' , "\n";
print '<div class="inner-wrap">' , "\n";
print '<nav class="top-bar tab-bar">' , "\n";

print '<!-- Title -->' , "\n";
print '<div class="large-4 medium-4 small-4 columns ">' , "\n";
print '<ul class="title-area">' , "\n";
print '<li class="name row"><h1><a href="index.html">' , "\n";
print '<span class="bacula-title">Bacula</span>' , "\n";
print '<span class="backups-title"> Backups</span></a></h1>' , "\n";
print '</li>' , "\n";
print '</ul>' , "\n";
print '</div>' , "\n";

print '<!-- Logo -->' , "\n";
print '<div class="large-4 columns hide-for-medium hide-for-small central-logo">' , "\n";
print '<img class="bacula_logo" src="img/logos/bacula_logo.png" alt="Bacula Backups">' , "\n";
print '</div>' , "\n";

print '<!-- Top Bar Right Nav Elements + Search -->' , "\n";
print '<div class="large-3 hide-for-small right search">' , "\n";
print '<div class="has-form">' , "\n";
print '<div class="row collapse">' , "\n";
print '<div class="large-10 medium-10  columns">' , "\n";
print '<input type="text" placeholder="Find">' , "\n";
print '</div>' , "\n";
print '<div class="large-2 medium-2  columns">' , "\n";
print '<a href="#" class="search button expand"><i class="fa fa-search fa-2x"></i></a>' , "\n";
print '</div>' , "\n";
print '</div>' , "\n";
print '</div>' , "\n";
print '</div>' , "\n";
print '<section class="right-small sidebar">' , "\n";
print '<a class="right-off-canvas-toggle" href="#"><i class="fa fa-reorder fa-2x sidebutton"></i></a>' , "\n";
print '</section>' , "\n";
print '</nav>' , "\n";

print '<aside class="right-off-canvas-menu">' , "\n";
print '<ul class="off-canvas-list">' , "\n";
print '<!--list header-->' , "\n";
print '<li><label><i class="fa fa-refresh fa-1x center refresh right"></i></label></li>' , "\n";
print '<!--search-->' , "\n";
print '<li class="show-for-small-only find"> ' , "\n";
print '<a href="#" class="width25"><i class="fa fa-search fa-1x small-6"></i></a>' , "\n";
print '<input type="text" class="small-6 width75" placeholder="Find">' , "\n";
print '</li>' , "\n";
print '<!--list body-->' , "\n";
print '<li><a href="#">System hostname</a></li>' , "\n";
print '<li><a href="#">Operating system</a></li>' , "\n";
print '<li><a href="#">Webmin version</a></li>' , "\n";
print '<li><a href="#">CPU load averages</a></li>' , "\n";
print '<li><a href="#">Real memory</a></li>' , "\n";
print '<li><a href="#">Virtual memory</a></li>' , "\n";
print '<li><a href="#">Local disk space</a></li>' , "\n";
print '<li class="service_stats_button"><a href="#extreme"><span class="service"> Service Stats</span> <span class="fa fa-arrow-down fa-1x service right"></span></a></li>' , "\n";
print '</ul>	' , "\n";
print '<!-- Buttons -->	' , "\n";
print '<!-- Triggers the modals -->' , "\n";
print '<div id="extreme" class="large-12 medium-12 small-12 restart_block">' , "\n";
print '<div class="large-4 medium-4 small-4 left"><a href="#" data-reveal-id="restart_service" class="button restart_bacula">Restart Bacula</a></div> ' , "\n";
print '<div class="large-4 medium-4 small-4 left"><a href="#" data-reveal-id="stop_service" class="button restart_bacula">Stop Bacula</a></div>' , "\n";
print '<div class="large-4 medium-4 small-4 left"><a href="#" data-reveal-id="start_service" class="button restart_bacula">Start at Boot</a></div>' , "\n";
print '<div class="large-12 medium-12 small-12 show-for-small-only left vi_logo_side">' , "\n";
print '<a href="http://www.versaointegral.pt"><img class="vi_logo"  src="img/logos/vi_logo.png" alt="Versão Integral"/></a>' , "\n";
print '</div>' , "\n";
print '</div>' , "\n";
print '<!-- Reveal Modals begin RESTART -->' , "\n";
print '<div id="restart_service" class="reveal-modal" data-reveal>' , "\n";
print '<h2>Wow! That\'s a little drastic...</h2>' , "\n";
print '<p>Restarting the service requires a brief unavailability of the system.</br>' , "\n";
print 'Confirming rhat you want to restart the service will stop and then start the system.</p>' , "\n";
print '<p><a href="#" data-reveal-id="restart_service_B" class="secondary button">Confirm</a></p>' , "\n";
print '<a class="close-reveal-modal right">&#215;</a>' , "\n";
print '</div>' , "\n";
print '<div id="restart_service_B" class="reveal-modal" data-reveal>' , "\n";
print '<h2>Here we go! You\'ve set the service to Restart!</h2>' , "\n";
print '<p>Your system will be restarted! Good luck :)</p>' , "\n";
print '<a class="close-reveal-modal">&#215;</a>' , "\n";
print '<!-- Reveal Modals begin STOP -->' , "\n";
print '<div id="stop_service" class="reveal-modal" data-reveal>' , "\n";
print '<h2>Are You Sure? That\'s a Huge step!</h2>' , "\n";
print '<p>Stoping the service will cause unavailability of the system.</br>' , "\n";
print 'Confirming rhat you want to <strong>stop the service</strong> will stop system.</p>' , "\n";
print '<p><a href="#" data-reveal-id="stop_service_B" class="secondary button">Confirm</a></p>' , "\n";
print '<a class="close-reveal-modal right">&#215;</a>' , "\n";
print '</div>' , "\n";
print '<div id="stop_service_B" class="reveal-modal" data-reveal>' , "\n";
print '<h2>You Did It! You\'ve Set the Service to Halt!</h2>' , "\n";
print '<p>Your system will stop! Good luck :)</p>' , "\n";
print '<a class="close-reveal-modal">&#215;</a>' , "\n";
print '</div>' , "\n";
print '<!-- Reveal Modals begin STOP -->' , "\n";
print '<div id="start_service" class="reveal-modal" data-reveal>' , "\n";
print '<h2>Do You Want To Set It All On Motion?</h2>' , "\n";
print '<p>Starting the service will activate the system.</br>' , "\n";
print 'Confirming rhat you want to <strong>start the service</strong> will set it all on.</p>' , "\n";
print '<p><a href="#" data-reveal-id="start_service_B" class="secondary button">Confirm</a></p>' , "\n";
print '<a class="close-reveal-modal right">&#215;</a>' , "\n";
print '</div>' , "\n";
print '<div id="start_service_B" class="reveal-modal" data-reveal>' , "\n";
print '<h2>Ignition! We Have Lift Off!</h2>' , "\n";
print '<p>Your system will start now! Good luck :)</p>' , "\n";
print '<a class="close-reveal-modal">&#215;</a>' , "\n";
print '</div>' , "\n";

print '</div>' , "\n";
print '</aside>' , "\n";

print '<!-- ##### corpo #####-->' , "\n";

print '<!--##############################################################################################################-->' , "\n";
print '<section class="main-section">' , "\n";
print '<!--##############################################################################################################-->     ' , "\n";

print '<!-- ##### main content #####-->' , "\n";

print '<section class="color_a">' , "\n";
print '<div class="row ">' , "\n";
print '<div class="large-12 medium-12 small-12 columns main-tittle text-center primeiro titulo arrow_box">' , "\n";
print 'Director Configuration' , "\n";
print '</div>' , "\n";
print '</div>' , "\n";

print '<div class="row"> ' , "\n";
print '<a href="#">' , "\n";
print '<div class="large-3 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-cog"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Director Configuration</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-3 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-users"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Backup Clients</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-3 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-file "></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">File Sets</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-3 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-clock-o"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Backup Schedules</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-4 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-calendar"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Backup Jobs</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-4 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-cubes"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Volume Pools</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-4 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-hdd-o "></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Storage Daemon</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";
print '</div>' , "\n";
print '</section>' , "\n";

print '<section class="color_b">' , "\n";

print '<div class="row ">' , "\n";
print '<div class="large-12 medium-12 small-12 columns main-tittle text-center titulo arrow_box">' , "\n";
print 'Storage Daemon Configuration' , "\n";
print '</div>' , "\n";
print '</div>' , "\n";

print '<div class="row">   ' , "\n";
print '<a href="#">' , "\n";
print '<div class="large-6 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-cog"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Storage Daemon Configuration</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-6 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-archive"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Storage Devices</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";
print '</div>' , "\n";
print '</section>' , "\n";

print '<section class="color_a">' , "\n";
print '<div class="row ">' , "\n";
print '<div class="large-12 medium-12 small-12 columns main-tittle text-center titulo arrow_box">' , "\n";
print 'File Daemong Config' , "\n";
print '</div>' , "\n";
print '</div>' , "\n";

print '<div class="row">' , "\n";
print '<a href="#">' , "\n";
print '<div class="large-12 medium-12 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-cog"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label"> File Daemong Config</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";
print '</section>' , "\n";

print '<section class="color_b">' , "\n";
print '<div class="row ">' , "\n";
print '<div class="large-12 medium-12 small-12 columns main-tittle text-center titulo arrow_box">' , "\n";
print 'Backup and Restore Actions' , "\n";
print '</div>' , "\n";
print '</div>  ' , "\n";

print '<div class="row">' , "\n";
print '<a href="#">' , "\n";
print '<div class="large-3 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-hdd-o"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Run Backup Job</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-3 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-user"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Director Status</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-3 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-info-circle"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Client Status</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-3 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-archive"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Storage Daemon Status</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-3 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-cube"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Label Volume</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-3 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-cubes"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Volumes in Pool</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-3 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-exchange"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Mount or Unmount</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '<a href="#">' , "\n";
print '<div class="large-3 medium-6 small-12 columns text-center padding_b_2rem">' , "\n";
print '<i class="fa fa-main fa-history"></i>' , "\n";
print '<div class="large-12 columns text-center fa-label">Restore Backup</div>' , "\n";
print '</div>' , "\n";
print '</a>' , "\n";

print '</section>' , "\n";
print '<!--##############################################################################################################-->' , "\n";
print '</section>' , "\n";
print '<a class="exit-off-canvas"></a>' , "\n";
print '<footer>' , "\n";
print '<div class="large-12 medium-12 small-12">' , "\n";
print '<div class="large-3 medium-4 hide-for-small-only columns">' , "\n";
print '<a href="http://www.versaointegral.pt"><img class="vi_logo" src="img/logos/vi_logo.png" alt="Versão Integral"/></a>' , "\n";
print '</div>' , "\n";
print '<div class="large-7 medium-4 small-8 columns user">' , "\n";
print 'Admnin@192.168.2.210' , "\n";
print '</div>' , "\n";
print '<a href="login.html"><div class="large-2 medium-4 small-4 columns logout">' , "\n";
print 'logout' , "\n";
print '</div></a>' , "\n";

print '</div>' , "\n";
print '</footer>  ' , "\n";
print '</div>' , "\n";

print '<!--##############################################################################################################-->' , "\n";

print '<script src="/unauthenticated/js/vendor/jquery.js"></script>' , "\n";
print '<script src="/unauthenticated/js/foundation.min.js"></script>' , "\n";
print '<script>' , "\n";
print <<ENDHTML
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

print '</body>' , "\n";
print '</html>' , "\n";
