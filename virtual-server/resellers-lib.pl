# Functions for managing resellers

# list_resellers()
# Returns a list of all reseller users. A reseller is a Webmin user with
# access to this module, and has the 'reseller' ACL option set
sub list_resellers
{
&require_acl();
local ($u, @rv);
foreach $u (&acl::list_users()) {
	if (&indexof($module_name, @{$u->{'modules'}}) >= 0) {
		local %acl = &get_reseller_acl($u->{'name'});
		if ($acl{'reseller'}) {
			local %gacl = &get_module_acl($u->{'name'}, "");
			$u->{'acl'} = \%acl;
			$u->{'acl'}->{'readonly'} = $gacl{'readonly'};
			push(@rv, $u);
			}
		}
	}
return @rv;
}

# get_reseller(name)
# Returns the hash for a reseller with a given name, or undef
sub get_reseller
{
local ($name) = @_;
&require_acl();
local @users = &acl::list_users();
local ($rv) = grep { $_->{'name'} eq $name } @users;
return undef if (!$rv || &indexof($module_name, @{$rv->{'modules'}}) < 0);
local %acl = &get_reseller_acl($name);
return undef if (!$acl{'reseller'});
$rv->{'acl'} = \%acl;
local %gacl = &get_module_acl($name, "");
$rv->{'acl'}->{'readonly'} = $gacl{'readonly'};
return $rv;
}

# create_reseller(&reseller, [plain-pass])
# Create a new reseller account, by adding the Webmin user
sub create_reseller
{
local ($resel, $plainpass) = @_;
&require_acl();
if (!$resel->{'modules'}) {
	$resel->{'modules'} = [ $module_name,
			       split(/\s+/, $config{'reseller_modules'}) ];
	# Grant other core modules. This still refers to the old avail_
	# config variabes, but thats OK as they get populated from the
	# default template.
	foreach my $m (@reseller_modules) {
		my $am = $m eq "bind8" ? "dns" : $m;
		push(@{$resel->{'modules'}}, $m) if ($config{'avail_'.$am});
		}

	# Grant modules from plugins
	my @doms = &get_reseller_domains($resel);
	if (@doms) {
		foreach my $p (@plugins) {
			my @pmods = &plugin_call($p, "feature_webmin",
						 $doms[0], \@doms);
			foreach my $pm (@pmods) {
				next if (!$config{'avail_'.$pm->[0]});
				push(@{$resel->{'modules'}}, $pm->[0]);
				if ($pm->[1]) {
					&save_module_acl(
					  $pm->[1], $resel->{'name'}, $pm->[0]);
					}
				}
			}
		}
	}
if (!exists($resel->{'theme'})) {
	$resel->{'theme'} = $config{'reseller_theme'} eq "*" ?
				undef : $config{'reseller_theme'};
	}
$resel->{'real'} = $resel->{'acl'}->{'desc'};
my $encpass = $resel->{'pass'};
if ($resel->{'acl'}->{'unix'}) {
	# Same as Unix
	$resel->{'pass'} = 'x';
	}
$resel->{'sync'} = 0;
$resel->{'cert'} = '';
&acl::create_user($resel);
$resel->{'acl'}->{'reseller'} = 1;
$resel->{'acl'}->{'noconfig'} = 1;
$resel->{'acl'}->{'stop'} = 0;
$resel->{'acl'}->{'local'} = 0;
$resel->{'acl'}->{'import'} = 0;
&save_module_acl($resel->{'acl'}, $resel->{'name'}, $module_name);
local %gacl = &get_module_acl($resel->{'name'}, "");
$gacl{'readonly'} = $resel->{'acl'}->{'readonly'};
$gacl{'fileunix'} = $resel->{'acl'}->{'unix'} ? $resel->{'name'} : 'nobody';
&save_module_acl(\%gacl, $resel->{'name'}, "");
&set_reseller_acl($resel);
&register_post_action(\&restart_webmin);

# If reseller wants a Unix user, create one
if ($resel->{'acl'}->{'unix'}) {
	&create_reseller_unix_user($resel, $encpass, $plainpass);
	}
}

# delete_reseller(&reseller)
# Remove a reseller account, and dis-associate any domains from it
sub delete_reseller
{
my ($resel) = @_;
&require_acl();
&acl::delete_user($resel->{'name'});
&register_post_action(\&restart_webmin);

# Take out of any domain groups
&update_reseller_unix_groups($resel, 0);

# Disconnect domains
foreach my $d (&get_reseller_domains($resel)) {
	my @r = split(/\s+/, $d->{'reseller'});
	@r = grep { $_ ne $resel->{'name'} } @r;
	$d->{'reseller'} = join(" ", @r);
	&save_domain($d);
	}

# Remove scheduled backups by the reseller
foreach my $sched (&list_scheduled_backups()) {
	if ($sched->{'owner'} eq $resel->{'name'}) {
		&delete_scheduled_backup($sched);
		}
	}

# Remove plans owned by reseller
foreach my $plan (&list_plans()) {
	if ($plan->{'owner'} eq $resel->{'name'}) {
		&delete_plan($plan);
		}
	}

# If there is a Unix user with the same name and in the resellers group,
# remove it
&delete_reseller_unix_user($resel);
}

# modify_reseller(&reseller, &old, [new-plaintext-pass])
# Updates a reseller Webmin user, and possibly any associated domains
sub modify_reseller
{
local ($resel, $old, $plainpass) = @_;
&require_acl();

# Grant or take away modules
foreach my $m (@reseller_modules) {
	my $am = $m eq "bind8" ? "dns" : $m;
	if ($config{'avail_'.$am}) {
		@{$resel->{'modules'}} = &unique(@{$resel->{'modules'}}, $m);
		}
	else {
		@{$resel->{'modules'}} = grep { $_ ne $m } @{$resel->{'modules'}};
		}
	}

# Grant modules from plugins
@{$resel->{'modules'}} = grep { &indexof($_, @plugins) < 0 }
			      @{$resel->{'modules'}};
my @doms = &get_reseller_domains($resel);
if (@doms) {
	foreach my $p (@plugins) {
		my @pmods = &plugin_call($p, "feature_webmin",
					 $doms[0], \@doms);
		foreach my $pm (@pmods) {
			next if (!$config{'avail_'.$pm->[0]});
			push(@{$resel->{'modules'}}, $pm->[0]);
			if ($pm->[1]) {
				&save_module_acl(
				  $pm->[1], $resel->{'name'}, $pm->[0]);
				}
			}
		}
	}

# Save the reseller's webmin user and ACL
$resel->{'real'} = $resel->{'acl'}->{'desc'};
&acl::modify_user($old->{'name'}, $resel);
&save_module_acl($resel->{'acl'}, $resel->{'name'}, $module_name);
local %gacl = &get_module_acl($resel->{'name'}, "");
$gacl{'readonly'} = $resel->{'acl'}->{'readonly'};
&save_module_acl(\%gacl, $resel->{'name'}, "");
&register_post_action(\&restart_webmin);

# Update any virtual servers that use the old reseller name
if ($resel->{'name'} ne $old->{'name'}) {
	foreach my $d (&get_reseller_domains($old->{'name'})) {
		my @r = split(/\s+/, $d->{'reseller'});
		my $idx = &indexof($old->{'name'}, @r);
		if ($idx >= 0) {
			$r[$idx] = $resel->{'name'};
			$d->{'reseller'} = join(" ", @r);
			&save_domain($d);
			}
		}
	}

# Update any plans owned by the reseller
if ($resel->{'name'} ne $old->{'name'}) {
	foreach my $plan (&list_plans()) {
		if ($plan->{'owner'} eq $old->{'name'}) {
			$plan->{'owner'} = $resel->{'name'};
			}
		local @prs = split(/\s+/, $plan->{'resellers'});
		local $idx = &indexof($old->{'name'}, @prs);
		if ($idx >= 0) {
			@prs[$idx] = $resel->{'name'};
			$plan->{'resellers'} = join(" ", @prs);
			}
		&save_plan($plan);
		}
	}

# Set Webmin ACL
&set_reseller_acl($resel);

# Create or delete reseller Unix user
if ($resel->{'acl'}->{'unix'} && !$old->{'acl'}->{'unix'}) {
	# Create Unix user, and re-save Webmin user with password sync enabled
	&create_reseller_unix_user($resel, $resel->{'pass'});
	$resel->{'pass'} = 'x';
	&acl::modify_user($resel->{'name'}, $resel);
	}
elsif (!$resel->{'acl'}->{'unix'} && $old->{'acl'}->{'unix'}) {
	# Remove the Unix user, and set 
	my $encpass = &delete_reseller_unix_user($resel);
	if ($encpass && $resel->{'pass'} eq 'x') {
		$resel->{'pass'} = $encpass;
		&acl::modify_user($resel->{'name'}, $resel);
		}
	}
elsif ($resel->{'acl'}->{'unix'} && $old->{'acl'}->{'unix'} &&
       ($resel->{'pass'} ne $old->{'pass'} ||
	$resel->{'acl'}->{'desc'} ne $old->{'acl'}->{'desc'})) {
	# May need to update password or description
	&update_reseller_unix_user($resel, $old, $plainpass);
	if ($resel->{'pass'} ne 'x') {
		$resel->{'pass'} = 'x';
		&acl::modify_user($resel->{'name'}, $resel);
		}
	}

# Update reseller membership of Unix groups
&update_reseller_unix_groups($resel, 1);
}

# set_reseller_acl(&reseller)
# Sets the reseller's ACL in other Webmin modules
sub set_reseller_acl
{
local ($resel) = @_;
local @doms = &get_reseller_domains($resel);

# Grant access to logs for domain owners
if (&indexof("webminlog", @{$resel->{'modules'}}) >= 0) {
	local %acl = ( 'rollback' => 0 );
	local @wdoms = grep { $_->{'webmin'} && !$_->{'parent'} } @doms;
	local @users = &unique(map { $_->{'user'} } @wdoms);
	$acl{'users'} = join(" ", $_[0]->{'name'}, @users);
	&save_module_acl(\%acl, $_[0]->{'name'}, "webminlog");
	}

# Grant access to domains' mailboxes
if (&indexof("mailboxes", @{$resel->{'modules'}}) >= 0) {
	local %acl = ( 'noconfig' => 1,
		       'fmode' => 1,
		       'from' => join(" ", map { $_->{'dom'} }
					       grep { $_->{'mail'} } @doms),
		       'canattach' => 0,
		       'candetach' => 0,
		       'dir' => &mail_domain_base($doms[0]),
		       'mmode' => 5,
		       'musers' => join(" ", &unique(map { $_->{'gid'} } @doms))
		     );
	&save_module_acl(\%acl, $_[0]->{'name'}, "mailboxes");
	}

# Grant access to DNS domains
if (&indexof("bind8", @{$resel->{'modules'}}) >= 0) {
        local %acl = ( 'noconfig' => 1,
                       'zones' => join(" ", map { $_->{'dom'} }
                                             grep { $_->{'dns'} } @doms),
                       'dir' => &resolve_links($doms[0]->{'home'}),
                       'master' => 0,
                       'slave' => 0,
                       'forward' => 0,
                       'delegation' => 0,
                       'defaults' => 0,
                       'reverse' => 0,
                       'multiple' => 1,
                       'ro' => 0,
                       'apply' => 2,
                       'file' => 0,
                       'params' => 1,
                       'opts' => 0,
                       'delete' => 0,
                       'gen' => 1,
                       'whois' => 1,
                       'findfree' => 1,
                       'slaves' => 0,
                       'remote' => 0,
                       'views' => 0,
                       'vlist' => '' );
	&save_module_acl(\%acl, $_[0]->{'name'}, "bind8");
	}

# Grant access to syslog logs for owned domains
if (&indexof("syslog", @{$resel->{'modules'}}) >= 0) {
	local @extras;
	local %done;
	foreach my $sd (@doms) {
		# Add Apache logs, for domains with websites and separate logs
		if ($sd->{'web'} && !$sd->{'alias_mode'}) {
			local $alog = &get_website_log($sd, 0);
			local $elog = &get_website_log($sd, 1);
			push(@extras, $alog." ".&text('webmin_alog',
						      $sd->{'dom'}))
				if ($alog && !$done{$alog}++);
			push(@extras, $elog." ".&text('webmin_elog',
						      $sd->{'dom'}))
				if ($elog && !$done{$elog}++);
			}
		# Add FTP logs
		if ($sd->{'ftp'}) {
			local $flog = &get_proftpd_log($sd->{'ip'});
			push(@extras, $flog." ".&text('webmin_flog',
						     $sd->{'dom'}))
				if ($flog && !$done{$flog}++);
			}
		}
	local %acl = ( 'extras' => join("\t", @extras),
		       'any' => 0,
		       'noconfig' => 1,
		       'noedit' => 1,
		       'syslog' => 0,
		       'others' => 0 );
	&save_module_acl_logged(\%acl, $_[0]->{'name'}, "syslog");
	}
}

# modify_all_resellers([&domain])
# Updates the Webmin users for all resellers (or just those who own some domain)
sub modify_all_resellers
{
local ($d) = @_;
local @resels = &list_resellers();
if ($d) {
	@resels = grep { &indexof($_->{'name'},
				split(/\s+/, $d->{'reseller'})) >= 0 } @resels;
	}
return if (!@resels);
&$first_print($text{'check_allresel'});
	{
	local ($first_print, $second_print, $indent_print, $outdent_print);
	&set_all_null_print();
	foreach my $r (@resels) {
		&modify_reseller($r, $r);
		}
	}
&$second_print($text{'setup_done'});
}

# send_reseller_email(&reseller, plainpass)
# Sends email to a new reseller. Returns a pair containing a
# number (0=failed, 1=success) and an optional message.
sub send_reseller_email
{
local ($resel, $plainpass) = @_;

# Get the email
&ensure_template("reseller-template");
return (1, undef) if ($config{'reseller_template'} eq 'none');
local $tmpl = $config{'reseller_template'} eq 'default' ?
	"$module_config_directory/reseller-template" :
	$config{'reseller_template'};

# Create reseller details hash
local %hash = %$resel;
$hash{'plainpass'} = $plainpass;
$hash{'email'} = $resel->{'acl'}->{'email'};
$hash{'desc'} = $resel->{'acl'}->{'desc'};

# Send it
local $subject = $config{'newreseller_subject'};
local $cc = $config{'newreseller_cc'};
local $cc = $config{'newreseller_bcc'};
return (1, undef) if (!$resel->{'acl'}->{'email'} && !$cc);
local @erv = &send_template_email(&cat_file($tmpl), $resel->{'acl'}->{'email'},
			    	  \%hash, $subject, $cc, $bcc);
}

# sync_parent_resellers([reseller])
# Update all sub-servers and set their resellers to match their parent domains
sub sync_parent_resellers
{
local ($resel) = @_;
local @alldoms = &list_domains();
local $count = 0;
foreach my $d (grep { !$_->{'parent'} } @alldoms) {
	next if (!$d->{'reseller'});
	next if ($resel && &indexof($resel,split(/\s+/, $d->{'reseller'})) < 0);
	foreach my $sd (grep { $_->{'parent'} eq $d->{'id'} } @alldoms) {
		if ($sd->{'reseller'} ne $d->{'reseller'}) {
			$sd->{'reseller'} = $d->{'reseller'};
			&save_domain($sd);
			$count++;
			}
		}
	}
return $count;
}

# get_reseller_domains(name)
# Return all domains a reseller can manager
sub get_reseller_domains
{
my ($name) = @_;
$name = $name->{'name'} if (ref($name));
my @rv;
foreach my $d (&list_domains()) {
	my @r = split(/\s+/, $d->{'reseller'});
	push(@rv, $d) if (&indexof($name, @r) >= 0);
	}
return @rv;
}

# create_reseller_unix_user(&reseller, encrypted-pass, [plaintext-pass])
# Create the Unix user for a reseller
sub create_reseller_unix_user
{
my ($resel, $encpass, $plainpass) = @_;
if (&is_hashed_password($plainpass)) {
	# Actually already hashed
	$plainpass = undef;
	}

# Create resellers group?
&require_useradmin();
&obtain_lock_unix();
local ($ginfo) = grep { $_->{'group'} eq $reseller_group_name }
		      &list_all_groups();
if (!$ginfo) {
	# Need to create
	local (%gtaken, %ggtaken);
	&build_group_taken(\%gtaken, \%ggtaken);
	local $gid = &allocate_gid(\%gtaken);
	$ginfo = { 'group' => $reseller_group_name,
		   'gid' => $gid };
	eval {
		local $main::error_must_die = 1;
		&foreign_call($usermodule, "set_group_envs", $ginfo,
			      'CREATE_GROUP');
		&foreign_call($usermodule, "making_changes");
		&foreign_call($usermodule, "create_group", $ginfo);
		&foreign_call($usermodule, "made_changes");
		};
	}

# Add the user
local (%taken, %utaken);
&build_taken(\%taken, \%utaken);
local $uid = &allocate_uid(\%taken);
local $shell = &default_available_shell('reseller') ||
	       &default_available_shell('owner');
local $home = &useradmin::auto_home_dir($home_base, $resel->{'name'},
					$ginfo->{'group'});
local $uinfo = { 'user' => $resel->{'name'},
		 'uid' => $uid,
		 'gid' => $ginfo->{'gid'},
		 'pass' => $plainpass ? 
			&useradmin::encrypt_password($plainpass) :
			$encpass,
		 'plainpass' => $plainpass,
		 'real' => $resel->{'real'},
		 'home' => $home,
		 'shell' => $shell };
eval {
	local $main::error_must_die = 1;
	&foreign_call($usermodule, "set_user_envs", $uinfo,
		      'CREATE_USER', $plainpass, [ ]);
	&foreign_call($usermodule, "making_changes");
	&foreign_call($usermodule, "create_user", $uinfo);
	&foreign_call($usermodule, "made_changes");
	};

# Create home dir
&useradmin::create_home_directory($uinfo);
local $uf = &useradmin::get_skel_directory($uinfo, $ginfo->{'group'});
&useradmin::copy_skel_files($uf, $uinfo->{'home'},
			    $uinfo->{'uid'}, $uinfo->{'gid'});

# Set secondary groups to match domains
&update_reseller_unix_groups($resel, 2);

&release_lock_unix();
}

# delete_reseller_unix_user(&resel)
# Delete the Unix user corresponding to a reseller, if there is one. Returns
# the user's encrypted password (if a user was found).
sub delete_reseller_unix_user
{
my ($resel) = @_;
&require_useradmin();
&obtain_lock_unix();
local ($ginfo) = grep { $_->{'group'} eq $reseller_group_name }
		      &list_all_groups();
local ($uinfo) = grep { $_->{'user'} eq $resel->{'name'} }
		      &list_all_users();
if ($ginfo && $uinfo && $uinfo->{'gid'} == $ginfo->{'gid'}) {
	# Found user to delete
	&foreign_call($uinfo->{'module'}, "set_user_envs",
		      $uinfo, 'DELETE_USER');
	&foreign_call($uinfo->{'module'}, "making_changes");
	&foreign_call($uinfo->{'module'}, "delete_user", $uinfo);
	&foreign_call($uinfo->{'module'}, "made_changes");

	# Delete home dir, if sane
	local $home = &useradmin::auto_home_dir($home_base, $resel->{'name'},
						$ginfo->{'group'});
	if ($home eq $uinfo->{'home'}) {
		&backquote_logged("rm -rf ".quotemeta($uinfo->{'home'}));
		}
	}
&release_lock_unix();
return $uinfo ? $uinfo->{'pass'} : undef;
}

# update_reseller_unix_user(&resel, &old-resel, [plainpass])
# Sync a reseller Unix user with the reseller Webmin user
sub update_reseller_unix_user
{
my ($resel, $old, $plainpass) = @_;
&require_useradmin();
&obtain_lock_unix();
local ($ginfo) = grep { $_->{'group'} eq $reseller_group_name }
		      &list_all_groups();
local ($uinfo) = grep { $_->{'user'} eq $resel->{'name'} }
		      &list_all_users();
if ($ginfo && $uinfo && $uinfo->{'gid'} == $ginfo->{'gid'}) {
	# Found user to update
	my $olduinfo = { %$uinfo };
	my $changed = 0;
	if ($uinfo->{'real'} ne $resel->{'acl'}->{'desc'}) {
		# Real name changed
		$uinfo->{'real'} = $resel->{'acl'}->{'desc'};
		$changed++;
		}
	if ($plainpass) {
		# Plain password set
		$uinfo->{'pass'} = &useradmin::encrypt_password($plainpass);
		$uinfo->{'passmode'} = 3;
		$changed++;
		}
	if ($changed) {
		local $main::error_must_die = 1;
		&foreign_call($usermodule, "set_user_envs", $uinfo,
			      'MODIFY_USER', $plainpass, [], $olduinfo);
		&foreign_call($usermodule, "making_changes");
		&foreign_call($usermodule, "modify_user", $olduinfo, $uinfo);
		&foreign_call($usermodule, "made_changes");
		}
	}
&release_lock_unix();
}

# update_reseller_unix_groups(&reseller, 0=deleting, 1=updating, 2=creating)
# Update all domain Unix groups for this reseller's domains to include the
# reseller Unix user, or not
sub update_reseller_unix_groups
{
my ($resel, $mode) = @_;
&require_useradmin();
&obtain_lock_unix();
local ($uinfo) = grep { $_->{'user'} eq $resel->{'name'} }
		      &list_all_users();
if ($uinfo) {
	# For each top-level domain, check if it's group contains this reseller
	local @glist = &list_all_groups();
	foreach my $d (&list_domains()) {
		next if ($d->{'parent'} || !$d->{'unix'});
		local ($ginfo) = grep { $_->{'group'} eq $d->{'group'} } @glist;
		next if (!$ginfo);
		local $oldginfo = { %$ginfo };
		local @members = split(/,/, $ginfo->{'members'});
		local @r = split(/\s+/, $d->{'reseller'});
		local $changed = 0;
		if ($mode == 0 &&
		    &indexof($resel->{'name'}, @members) >= 0) {
			# Deleting reseller, so always remove from the group
			@members = grep { $_ ne $resel->{'name'} } @members;
			$changed++;
			}
		elsif ($mode > 0 &&
		       &indexof($resel->{'name'}, @members) < 0 &&
		       &indexof($resel->{'name'}, @r) >= 0) {
			# Reseller is not in the group, but should be
			push(@members, $resel->{'name'});
			$changed++;
			}
		elsif ($mode > 0 &&
		       &indexof($resel->{'name'}, @members) >= 0 &&
		       &indexof($resel->{'name'}, @r) < 0) {
			# Reseller is in the group, but should not be
			@members = grep { $_ ne $resel->{'name'} } @members;
			$changed++;
			}
		if ($changed) {
			# Update group membership list
			$ginfo->{'members'} = join(",", @members);
			&foreign_call($ginfo->{'module'}, "set_group_envs",
				      $ginfo, 'MODIFY_GROUP', $oldginfo);
			&foreign_call($ginfo->{'module'}, "making_changes");
			&foreign_call($ginfo->{'module'}, "modify_group",
				      $oldginfo, $ginfo);
			&foreign_call($ginfo->{'module'}, "made_changes");
			}
		}
	}
&release_lock_unix();
}

# set_reseller_envs(&reseller, action)
# Set environment variables before running a reseller command
sub set_reseller_envs
{
local ($resel, $action) = @_;
$ENV{'RESELLER_ACTION'} = $action;
$ENV{'RESELLER_NAME'} = $resel->{'name'};
$ENV{'RESELLER_EMAIL'} = $resel->{'acl'}->{'email'};
$ENV{'RESELLER_DESC'} = $resel->{'acl'}->{'desc'};
my @rdoms = &get_reseller_domains($resel);
$ENV{'RESELLER_DOMS'} = join(" ", map { $_->{'dom'} } @rdoms);
}

# execute_before_reseller(&reseller, action)
# Runs any command configured to be run before a reseller is changed
sub execute_before_reseller
{
local ($resel, $action) = @_;
return undef if (!$config{'reseller_pre_command'});
&clean_changes_environment();
&set_reseller_envs($resel, $action);
my $out = &backquote_logged(
	"($config{'reseller_pre_command'}) 2>&1 </dev/null");
&reset_changes_environment();
return $? ? $out : undef;
}

# execute_after_reseller(&reseller, action)
# Runs any command configured to be run after a reseller is changed
sub execute_after_reseller
{
local ($resel, $action) = @_;
return undef if (!$config{'reseller_post_command'});
&clean_changes_environment();
&set_reseller_envs($resel, $action);
my $out = &backquote_logged(
	"($config{'reseller_post_command'}) 2>&1 </dev/null");
&reset_changes_environment();
return $? ? $out : undef;
}

1;

