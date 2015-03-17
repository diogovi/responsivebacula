#!/usr/bin/perl
BEGIN { push(@INC, ".."); };
use WebminCore;
&ReadParse();
&init_config();
&load_theme_library();
if (&get_product_name() eq "usermin") {
	$level = 3;
}
else {
	$level = 0;
}
%text = &load_language($current_theme);
&header($title);
print '<div id="wrapper" class="page">' . "\n";
print '<div class="container">' . "\n";
print '<div id="system-status" class="panel panel-default" style="margin-top: 20px">' . "\n";
print '<div class="panel-heading">' . "\n";
print '<h3 class="panel-title">' . &text('body_header0') . '</h3>' . "\n";
print '</div>';
print '<div class="panel-body">' . "\n";
if ($level == 0) {
	# Ask status module for collected info
	&foreign_require("system-status");
	$info = &system_status::get_collected_info();
	# Circle Progress Container
	print '<div class="row" style="margin: 0;">' . "\n";
	$col_width = &get_col_num($info, 12);
	# CPU Usage
	if ($info->{'cpu'}) {
		@c = @{$info->{'cpu'}};
		$used = $c[0]+$c[1]+$c[3];
		&print_progressbar_colum(6, $col_width, $used, 'CPU');
	}
	# MEM e VIRT Usage
	if ($info->{'mem'}) {
		@m = @{$info->{'mem'}};
		if (@m && $m[0]) {
			$used = ($m[0]-$m[1])/$m[0]*100;
			&print_progressbar_colum(6, $col_width, $used, 'MEM');
		}
		if (@m && $m[2]) {
			$used = ($m[2]-$m[3])/$m[2]*100;
			&print_progressbar_colum(6, $col_width, $used, 'VIRT');
		}
	}
	# HDD Usage
	if ($info->{'disk_total'}) {
		($total, $free) = ($info->{'disk_total'}, $info->{'disk_free'});
		$used = ($total-$free)/$total*100;
		&print_progressbar_colum(6, $col_width, $used, 'HDD');
	}
	print '</div>' . "\n";
	# Info table 
	print '<table class="table table-hover">' . "\n";
	# Hostname Info
	$ip = $info && $info->{'ips'} ? $info->{'ips'}->[0]->[0] : &to_ipaddress(get_system_hostname());
	$ip = " ($ip)" if ($ip);
	$host = &get_system_hostname() . $ip;
	if (&foreign_available("net")) {
		$host = '<a href="net/list_dns.cgi">' . $host . '</a>';
	}
	&print_table_row(&text('body_host'), $host);
	# Operating System Info
	if ($gconfig{'os_version'} eq '*') {
		$os = $gconfig{'real_os_type'};
	} else {
		$os = $gconfig{'real_os_type'} . ' ' . $gconfig{'real_os_version'};
	}
	&print_table_row(&text('body_os'), $os);
	# Webmin version
	&print_table_row(&text('body_webmin'), &get_webmin_version());
	#System Time
	$tm = localtime(time());
	if (&foreign_available("time")) {
		$tm = '<a href=time/>' . $tm . '</a>';
	}
	&print_table_row(&text('body_time'), $tm);
	# Kernel and CPU Info
	if ($info->{'kernel'}) {
		&print_table_row(&text('body_kernel'), &text('body_kernelon', $info->{'kernel'}->{'os'}, $info->{'kernel'}->{'version'}, $info->{'kernel'}->{'arch'}));
	}
	# CPU Type and cores
	if ($info->{'load'}) {
		@c = @{$info->{'load'}};
		if (@c > 3) {
			&print_table_row($text{'body_cpuinfo'}, &text('body_cputype', @c));
		}
	}
	# Temperatures Info (if available)
	if ($info->{'cputemps'}) {
		foreach my $t (@{$info->{'cputemps'}}) {
			$cputemp .= 'Core ' . $t->{'core'} . ': ' . int($t->{'temp'}) . '&#176;C<br>';
		}
		&print_table_row($text{'body_cputemps'}, $cputemp);
	}
	if ($info->{'drivetemps'}) {
		foreach my $t (@{$info->{'drivetemps'}}) {
			my $short = $t->{'device'};
			$short =~ s/^\/dev\///;
			my $emsg;
			if ($t->{'errors'}) {
				$emsg .= ' (<span class="text-danger">' . &text('body_driveerr', $t->{'errors'}) . "</span>)";
			}
			elsif ($t->{'failed'}) {
				$emsg .= ' (<span class="text-danger">' . &text('body_drivefailed') . '</span>)';
			}
			$hddtemp .= $short .  ': ' . int($t->{'temp'}) . '&#176;C<br>' . $emsg;
		}
		&print_table_row($text{'body_drivetemps'}, $hddtemp);
	}
	# System uptime
	&foreign_require("proc");
	my $uptime;
	my ($d, $h, $m) = &proc::get_system_uptime();
	if ($d) {
		$uptime = &text('body_updays', $d, $h, $m);
	}
	elsif ($m) {
		$uptime = &text('body_uphours', $h, $m);
	}
	elsif ($m) {
		$uptime = &text('body_upmins', $m);
	}
	if ($uptime) {
		if (&foreign_available("init")) {
			$uptime = '<a href=init/>' . $uptime . '</a>';
		}
		&print_table_row($text{'body_uptime'}, $uptime);
	}
	# Running processes
	if (&foreign_check("proc")) {
		@procs = &proc::list_processes();
		$pr = scalar(@procs);
		if (&foreign_available("proc")) {
			$pr = '<a href=proc/>' . $pr . '</a>';
		}
		&print_table_row($text{'body_procs'}, $pr);
	}
	# Load averages
	if ($info->{'load'}) {
		@c = @{$info->{'load'}};
		if (@c) {
			&print_table_row($text{'body_cpu'}, &text('body_load', @c));
		}
	}
	# Package updates
	if ($info->{'poss'}) {
		@poss = @{$info->{'poss'}};
		@secs = grep { $_->{'security'} } @poss;
		if (@poss && @secs) {
			$msg = &text('body_upsec', scalar(@poss), scalar(@secs));
		}
		elsif (@poss) {
			$msg = &text('body_upneed', scalar(@poss));
		}
		else {
			$msg = $text{'body_upok'};
		}
		if (&foreign_available("package-updates")) {
			$msg = '<a href="package-updates/index.cgi?mode=updates">' . $msg  . '</a>';
		}
		&print_table_row($text{'body_updates'}, $msg);
	}
	print '</table>' . "\n";
	# Webmin notifications
	print '</div>' . "\n";
	if (&foreign_check("webmin")) {
		&foreign_require("webmin", "webmin-lib.pl");
		my @notifs = &webmin::get_webmin_notifications();
		if (@notifs) {
			print '<div class="panel-footer">' . "\n";
			print "<center>\n",join("<hr>\n", @notifs),"</center>\n";
			print '</div>' . "\n";
		}
		# print scalar(@notifs);
	}
} elsif ($level == 3) {
	print '<table class="table table-hover">' . "\n";
	# Host and login info
	&print_table_row(&text('body_host'), &get_system_hostname());
	# Operating System Info
	if ($gconfig{'os_version'} eq '*') {
		$os = $gconfig{'real_os_type'};
	} else {
		$os = $gconfig{'real_os_type'} . ' ' . $gconfig{'real_os_version'};
	}
	&print_table_row(&text('body_os'), $os);
	# Webmin version
	&print_table_row(&text('body_usermin'), &get_webmin_version());
	#System Time
	$tm = localtime(time());
	if (&foreign_available("time")) {
		$tm = '<a href=time/>' . $tm . '</a>';
	}
	&print_table_row(&text('body_time'), $tm);
	# Disk quotas -- !!!!!
	if (&foreign_installed("quota")) {
		&foreign_require("quota", "quota-lib.pl");
		$n = &quota::user_filesystems($remote_user);
		$usage = 0;
		$quota = 0;
		for($i=0; $i<$n; $i++) {
			if ($quota::filesys{$i,'hblocks'}) {
				$quota += $quota::filesys{$i,'hblocks'};
				$usage += $quota::filesys{$i,'ublocks'};
			}
			elsif ($quota::filesys{$i,'sblocks'}) {
				$quota += $quota::filesys{$i,'sblocks'};
				$usage += $quota::filesys{$i,'ublocks'};
			}
		}
		if ($quota) {
			$bsize = $quota::config{'block_size'};
			print '<tr>' . "\n";
			print '<td><strong>' . $text{'body_uquota'} . '</strong></td>' . "\n";
			print '<td>' . &text('right_out', &nice_size($usage*$bsize), &nice_size($quota*$bsize)), '</td>' . "\n";
			print '</tr>' . "\n";
			print '<tr>' . "\n";
			print '<td></td>' . "\n";
			print '<td>' . "\n";
			print '<div class="progress">' . "\n";
			$used = $usage/$quota*100;
			print '<div class="progress-bar progress-bar-info" role="progressbar" aria-valuenow="' . $used . '" aria-valuemin="0" aria-valuemax="100" style="width: ' . $used . '%">' . "\n";
			print '</div>' . "\n";
			print '</div>' . "\n";
			print '</td>' . "\n";
			print '</tr>' . "\n";
		}
	}
	print '</table>' . "\n";
}
# End of page
print '</div>' . "\n";
#print '<p id="about">Template developed and written by <a href="https://www.facebook.com/RiccardoNob" target="_blank">Riccardo Nobile</a> & <a href="https://www.facebook.com/simone.cragnolini" target="_blank">Simone Cragnolini</a></p>' . "\n";
#print '<p id="about"><a href="http://winfuture.it/" target="_blank">WinFuture</a></p>' . "\n";
print '</div>' . "\n";
#print '</div>' . "\n";
&footer();

sub print_progressbar_colum {
	my ($xs, $sm, $percent, $label) = @_;
	use POSIX;
	$percent = ceil($percent);
	if ($percent < 75) {
		$class = 'success';
	} elsif ($percent < 90) {
		$class = 'warning';
	} else {
		$class = 'danger';
	}
	print '<div class="col-xs-' . $xs . ' col-sm-' . $sm . '">' . "\n";
	print '<div data-progress="' . $percent . '" class="progress progress-circle">' . "\n";
	print '<div class="progress-bar-circle progress-bar-' . $class . '">' . "\n";
	print '<div class="progress-bar-circle-mask progress-bar-circle-full">' . "\n";
	print '<div class="progress-bar-circle-fill"></div>' . "\n";
	print '</div>' . "\n";
	print '<div class="progress-bar-circle-mask progress-bar-circle-half">' . "\n";
	print '<div class="progress-bar-circle-fill"></div>' . "\n";
	print '<div class="progress-bar-circle-fill progress-bar-circle-fix"></div>' . "\n";
	print '</div>' . "\n";
	print '<div class="progress-bar-circle-inset">' . "\n";
	print '<div class="progress-bar-circle-title">' . "\n";
	print '<strong class="text-muted">' . $label . '</strong>' . "\n";
	print '</div>' . "\n";
	print '<div class="progress-bar-circle-percent">' . "\n";
	print '<span></span>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
}

sub get_col_num {
	my ($info, $max_col) = @_;
	my $num_col = 0;
	if ($info->{'cpu'}) { $num_col++; }
	if ($info->{'mem'}) {
		@m = @{$info->{'mem'}};
		if (@m && $m[0]) { $num_col++; }
		if (@m && $m[2]) { $num_col++; }
	}
	if ($info->{'disk_total'}) { $num_col++; }
	my $col = $max_col / $num_col;
	return $col;
}

sub print_table_row {
	local ($title, $content) = @_;
	print '<tr>' . "\n";
	print '<td><strong>' . $title . '</strong></td>' . "\n";
	print '<td>' . $content . '</td>' . "\n";
	print '</tr>' . "\n";
}