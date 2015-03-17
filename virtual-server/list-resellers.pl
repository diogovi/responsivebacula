#!/usr/bin/perl

=head1 list-resellers.pl

List existing resellers

When run with no parameters, this program simply displays a reader-friendly
table of existing Virtualmin resellers. The only supported options are
C<--multiline>, which causes it to show more details about each reseller in a
format suitable for reading by other programs, and C<--name-only> to dump
just a list of reseller usernames.

=cut

package virtual_server;
if (!$module_name) {
	$main::no_acl_check++;
	$ENV{'WEBMIN_CONFIG'} ||= "/etc/webmin";
	$ENV{'WEBMIN_VAR'} ||= "/var/webmin";
	if ($0 =~ /^(.*)\/[^\/]+$/) {
		chdir($pwd = $1);
		}
	else {
		chop($pwd = `pwd`);
		}
	$0 = "$pwd/list-resellers.pl";
	require './virtual-server-lib.pl';
	$< == 0 || die "list-resellers.pl must be run as root";
	}
use POSIX;

# Parse command-line args
$owner = 1;
while(@ARGV > 0) {
	local $a = shift(@ARGV);
	if ($a eq "--multiline") {
		$multi = 1;
		}
	elsif ($a eq "--name-only") {
		$nameonly = 1;
		}
	elsif ($a eq "--name") {
		$name = shift(@ARGV);
		}
	else {
		&usage("Unknown parameter $a");
		}
	}

# Get all resellers
@resels = &list_resellers();
@resels = sort { $a->{'name'} cmp $b->{'name'} } @resels;
if ($name) {
	@resels = grep { $_->{'name'} eq $name } @resels;
	@resels || &usage("No reseller named $name exists");
	}

# Get counts for each
foreach $r (@resels) {
	my @rdoms = &get_reseller_domains($r);
	$quota = 0;
	foreach $d (@rdoms) {
		$quota += $d->{'quota'};
		}
	$r->{'doms'} = \@rdoms;
	$r->{'quota'} = $quota;
	}

if ($multi) {
	# Show attributes on multiple lines
	$home_bsize = &has_home_quotas() ? &quota_bsize("home") : 0;
	foreach $r (@resels) {
		$acl = $r->{'acl'};
		print "$r->{'name'}\n";
		print "    Description: $r->{'acl'}->{'desc'}\n";
		if ($r->{'acl'}->{'email'}) {
			print "    Email: $r->{'acl'}->{'email'}\n";
			}
		print "    Login: ",
			($r->{'pass'} =~ /^\!/ ? "Disabled" : "Enabled"),"\n";
		foreach $m (@reseller_maxes) {
			$got = &count_domain_feature($m, @{$r->{'doms'}});
			$desc = $m eq "doms" ? "domains" :
				$m eq "aliasdoms" ? "alias domains" :
				$m eq "realdoms" ? "real domains" :
				$m eq "quota" ? "disk quota" :
				$m eq "mailboxes" ? "mailboxes" :
				$m eq "bw" ? "bandwidth" :
				$m eq "dbs" ? "databases" : $m;
			next if ($m eq "quota" && !$home_bsize);
			if ($m eq "quota") {
				$max = $acl->{'max_'.$m};
				print "    Maximum $desc: ",
				   ($max eq "" ? "Unlimited" :
					&quota_show($max, "home")),"\n";
				print "    Current $desc: ",
				   ($got < 0 ? "Unlimited" :
				      &quota_show($got, "home")),"\n";
				print "    Maximum byte $desc: ",
				   ($max eq "" ? "Unlimited" :
					$max * $home_bsize),"\n";
				print "    Current byte $desc: ",
				      ($got < 0 ? "Unlimited" :
					$got * $home_bsize),"\n";
				}
			else {
				print "    Maximum $desc: ".
				   ($acl->{'max_'.$m} eq "" ? "Unlimited" :
					$acl->{'max_'.$m})."\n";
				print "    Current $desc: $got\n";
				}
			}
		print "    Allowed features: ",join(" ", grep { $acl->{'feature_'.$_} } &list_allowable_features()),"\n";
		print "    Owned servers: ",join(" ", map { $_->{'dom'} } @{$r->{'doms'}}),"\n";
		print "    Read-only mode: ",($acl->{'readonly'} ? "Yes" : "No"),"\n";
		print "    Hide limits from server admins: ",($acl->{'hide'} ? "Yes" : "No"),"\n";
		if ($acl->{'subdom'}) {
			print "    Limit virtual servers to domain: ",
				$acl->{'subdom'},"\n";
			}
		if ($acl->{'logo'}) {
			print "    Logo URL: $acl->{'logo'}\n";
			if ($acl->{'link'}) {
				print "    Logo link: $acl->{'link'}\n";
				}
			}
		if ($acl->{'defip'}) {
			print "    Name-based IP address: $acl->{'defip'}\n";
			}
		if ($acl->{'defip6'}) {
			print "    Name-based IPv6 address: $acl->{'defip6'}\n";
			}
		print "    Can select shared IPs: ",
			($acl->{'nosharedips'} ? "No" : "Yes"),"\n";
		if ($acl->{'defdnsip'}) {
			print "    External IP address: $acl->{'defdnsip'}\n";
			}
		if ($acl->{'defns'}) {
			print "    Custom nameservers: $acl->{'defns'}\n";
			}
		print "    Can create plans: ",
			$acl->{'noplans'} ? "No" : "Yes","\n";
		print "    Can create and edit resellers: ",
			$acl->{'createresellers'} ? "Yes" : "No","\n";
		print "    Can create backups: ",
			$acl->{'backups'} == 2 ? "Schedule and make" :
			$acl->{'backups'} == 1 ? "Make only" : "No","\n";
		if ($acl->{'ranges'}) {
			foreach $r (&parse_ip_ranges($acl->{'ranges'})) {
				print "    IPv4 allocation range: ".
					$r->[0]."-".$r->[1].
					($r->[2] ? "/".$r->[2] : "")."\n";
				}
			}
		if ($acl->{'ranges6'}) {
			foreach $r (&parse_ip_ranges($acl->{'ranges6'})) {
				print "    IPv6 allocation range: ".
					$r->[0]."-".$r->[1].
					($r->[2] ? "/".$r->[2] : "")."\n";
				}
			}
		}
	}
elsif ($nameonly) {
	# Just reseller usernames
	foreach $r (@resels) {
		print $r->{'name'},"\n";
		}
	}
else {
	# Just show summary table
	$fmt = "%-15.15s %-30.30s %-15.15s %-15.15s\n";
	printf $fmt, "Name", "Description", "Domains", "Quota";
	printf $fmt, ("-" x 15), ("-" x 30), ("-" x 15), ("-" x 15);
	foreach $r (@resels) {
		$domsmax = $r->{'acl'}->{'max_doms'} ne "" ?
				"Max ".$r->{'acl'}->{'max_doms'} :
				"No limit";
		$quotamax = $r->{'acl'}->{'max_quota'} ?
			"Max ".&quota_show($r->{'acl'}->{'max_quota'}, "home") :
			"No limit";
		printf $fmt, $r->{'name'}, $r->{'acl'}->{'desc'},
			     scalar(@{$r->{'doms'}})." ($domsmax)",
			     &quota_show($r->{'quota'}, "home")." ($quotamax)";
		}
	}

sub usage
{
print "$_[0]\n\n" if ($_[0]);
print "Lists the resellers on this system.\n";
print "\n";
print "virtualmin list-resellers [--multiline | --name-only]\n";
print "                          [--name username]\n";
exit(1);
}


