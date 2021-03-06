#!/usr/bin/perl
# save_user.cgi
# Save, create or delete a user

require './mysql-lib.pl';
&ReadParse();
$access{'perms'} == 1 || &error($text{'perms_ecannot'});

if ($in{'delete'}) {
	# Delete some user
	&execute_sql_logged($master_db,
		     "delete from user where user = '$in{'olduser'}' ".
		     "and host = '$in{'oldhost'}'");
	}
else {
	# Validate inputs
	&error_setup($text{'user_err'});
	$in{'mysqluser_def'} || $in{'mysqluser'} =~ /^\S+$/ ||
		&error($text{'user_euser'});
	$in{'host_def'} || $in{'host'} =~ /^\S+$/ ||
		&error($text{'user_ehost'});

	map { $perms[$_]++ } split(/\0/, $in{'perms'});
	@desc = &table_structure($master_db, 'user');
	%fieldmap = map { $_->{'field'}, $_->{'index'} } @desc;
	$host = $in{'host_def'} ? '%' : $in{'host'};
	$user = $in{'mysqluser_def'} ? '' : $in{'mysqluser'};
	if ($in{'new'}) {
		# Create a new user
		for($i=3; $i<=&user_priv_cols()+3-1; $i++) {
			push(@yesno, $perms[$i] ? "'Y'" : "'N'");
			}
		foreach my $f ('ssl_type', 'ssl_cipher',
			       'x509_issuer', 'x509_subject', 'plugin',
			       'authentication_string') {
			if ($fieldmap{$f}) {
				push(@ssl_field_names, $f);
				push(@ssl_field_values, "''");
				}
			}
		$sql = sprintf "insert into user (%s) values ('%s', '%s', '', %s)",
			join(",", (map { $desc[$_]->{'field'} }
				      (0 .. &user_priv_cols()+3-1)),
				  @ssl_field_names),
			$host, $user,
			join(",", @yesno, @ssl_field_values);
		}
	else {
		# Update existing user
		for($i=3; $i<=&user_priv_cols()+3-1; $i++) {
			push(@yesno, $desc[$i]->{'field'}."=".
				     ($perms[$i] ? "'Y'" : "'N'"));
			}
		$sql = sprintf "update user set host = '%s', user = '%s', ".
			       "%s where user = '%s' and host = '%s'",
		    $host, $user,
		    join(" , ", @yesno), $in{'olduser'}, $in{'oldhost'};
		}
	&execute_sql_logged($master_db, $sql);
	if ($in{'mysqlpass_mode'} == 0) {
		$esc = &escapestr($in{'mysqlpass'});
		&execute_sql_logged($master_db,
			"update user set password = $password_func('$esc') ".
			"where user = ? and host = ?",
			$user, $host);
		}
	elsif ($in{'mysqlpass_mode'} == 2) {
		&execute_sql_logged($master_db,
			"update user set password = NULL ".
			"where user = ? and host = ?",
			$user, $host);
		}

	# Save various limits
	foreach $f ('max_user_connections', 'max_connections',
		    'max_questions', 'max_updates') {
		next if ($mysql_version < 5 || !defined($in{$f.'_def'}));
		$in{$f.'_def'} || $in{$f} =~ /^\d+$/ ||
		       &error($text{'user_e'.$f});
		&execute_sql_logged($master_db,
			"update user set $f = ? ".
			"where user = ? and host = ?",
			$in{$f.'_def'} ? 0 : $in{$f}, $user, $host);
		}

	# Set SSL fields
	if ($mysql_version >= 5 && defined($in{'ssl_type'})) {
		&execute_sql_logged($master_db,
			"update user set ssl_type = ? and ssl_cipher = ? ".
			"where user = ? and host = ?",
			$in{'ssl_type'}, $in{'ssl_cipher'}, $user, $host);
		}
	}
&execute_sql_logged($master_db, 'flush privileges');
if (!$in{'delete'} && !$in{'new'} &&
    $in{'olduser'} eq $config{'login'} && !$access{'user'}) {
	# Renamed or changed the password for the Webmin login .. update
	# it too!
	$config{'login'} = $in{'mysqluser'};
	if ($in{'mysqlpass_mode'} == 0) {
		$config{'pass'} = $in{'mysqlpass'};
		}
	elsif ($in{'mysqlpass_mode'} == 2) {
		$config{'pass'} = undef;
		}
	&lock_file($module_config_file);
	&save_module_config();
	&unlock_file($module_config_file);
	}
if ($in{'delete'}) {
	&webmin_log("delete", "user", $in{'olduser'},
		    { 'user' => $in{'olduser'},
		      'host' => $in{'oldhost'} } );
	}
elsif ($in{'new'}) {
	&webmin_log("create", "user",
		    $in{'mysqluser_def'} ? '' : $in{'mysqluser'},
		    { 'user' => $in{'mysqluser_def'} ? '' : $in{'mysqluser'},
		      'host' => $in{'host_def'} ? '' : $in{'host'} } );
	}
else {
	&webmin_log("modify", "user",
		    $in{'mysqluser_def'} ? '' : $in{'mysqluser'},
		    { 'user' => $in{'mysqluser_def'} ? '' : $in{'mysqluser'},
		      'host' => $in{'host_def'} ? '' : $in{'host'} } );
	}
&redirect("list_users.cgi");

