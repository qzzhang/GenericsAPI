package GenericsAPI::GenericsAPIClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

GenericsAPI::GenericsAPIClient

=head1 DESCRIPTION


A KBase module: GenericsAPI


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => GenericsAPI::GenericsAPIClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 fetch_data

  $returnVal = $obj->fetch_data($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a GenericsAPI.FetchDataParams
$returnVal is a GenericsAPI.FetchDataReturn
FetchDataParams is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a GenericsAPI.obj_ref
	generics_module has a value which is a reference to a hash where the key is a string and the value is a string
obj_ref is a string
FetchDataReturn is a reference to a hash where the following keys are defined:
	data_matrix has a value which is a string

</pre>

=end html

=begin text

$params is a GenericsAPI.FetchDataParams
$returnVal is a GenericsAPI.FetchDataReturn
FetchDataParams is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a GenericsAPI.obj_ref
	generics_module has a value which is a reference to a hash where the key is a string and the value is a string
obj_ref is a string
FetchDataReturn is a reference to a hash where the following keys are defined:
	data_matrix has a value which is a string


=end text

=item Description

fetch_data: fetch generics data as pandas dataframe for a generics data object

=back

=cut

 sub fetch_data
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function fetch_data (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to fetch_data:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'fetch_data');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "GenericsAPI.fetch_data",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'fetch_data',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method fetch_data",
					    status_line => $self->{client}->status_line,
					    method_name => 'fetch_data',
				       );
    }
}
 


=head2 generate_matrix_html

  $returnVal = $obj->generate_matrix_html($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a GenericsAPI.GenMatrixHTMLParams
$returnVal is a GenericsAPI.GenMatrixHTMLReturn
GenMatrixHTMLParams is a reference to a hash where the following keys are defined:
	df has a value which is a reference to a hash where the key is a string and the value is a string
GenMatrixHTMLReturn is a reference to a hash where the following keys are defined:
	html_string has a value which is a string

</pre>

=end html

=begin text

$params is a GenericsAPI.GenMatrixHTMLParams
$returnVal is a GenericsAPI.GenMatrixHTMLReturn
GenMatrixHTMLParams is a reference to a hash where the following keys are defined:
	df has a value which is a reference to a hash where the key is a string and the value is a string
GenMatrixHTMLReturn is a reference to a hash where the following keys are defined:
	html_string has a value which is a string


=end text

=item Description

generate_matrix_html: generate a html page for given data

=back

=cut

 sub generate_matrix_html
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function generate_matrix_html (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to generate_matrix_html:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'generate_matrix_html');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "GenericsAPI.generate_matrix_html",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'generate_matrix_html',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method generate_matrix_html",
					    status_line => $self->{client}->status_line,
					    method_name => 'generate_matrix_html',
				       );
    }
}
 


=head2 export_matrix

  $returnVal = $obj->export_matrix($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a GenericsAPI.ExportParams
$returnVal is a GenericsAPI.ExportOutput
ExportParams is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a GenericsAPI.obj_ref
	generics_module has a value which is a reference to a hash where the key is a string and the value is a string
obj_ref is a string
ExportOutput is a reference to a hash where the following keys are defined:
	shock_id has a value which is a string

</pre>

=end html

=begin text

$params is a GenericsAPI.ExportParams
$returnVal is a GenericsAPI.ExportOutput
ExportParams is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a GenericsAPI.obj_ref
	generics_module has a value which is a reference to a hash where the key is a string and the value is a string
obj_ref is a string
ExportOutput is a reference to a hash where the following keys are defined:
	shock_id has a value which is a string


=end text

=item Description



=back

=cut

 sub export_matrix
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function export_matrix (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to export_matrix:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'export_matrix');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "GenericsAPI.export_matrix",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'export_matrix',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method export_matrix",
					    status_line => $self->{client}->status_line,
					    method_name => 'export_matrix',
				       );
    }
}
 


=head2 validate_data

  $returnVal = $obj->validate_data($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a GenericsAPI.ValidateParams
$returnVal is a GenericsAPI.ValidateOutput
ValidateParams is a reference to a hash where the following keys are defined:
	obj_type has a value which is a string
	data has a value which is a reference to a hash where the key is a string and the value is a string
ValidateOutput is a reference to a hash where the following keys are defined:
	validated has a value which is a GenericsAPI.boolean
	failed_constraint has a value which is a reference to a hash where the key is a string and the value is a string
boolean is an int

</pre>

=end html

=begin text

$params is a GenericsAPI.ValidateParams
$returnVal is a GenericsAPI.ValidateOutput
ValidateParams is a reference to a hash where the following keys are defined:
	obj_type has a value which is a string
	data has a value which is a reference to a hash where the key is a string and the value is a string
ValidateOutput is a reference to a hash where the following keys are defined:
	validated has a value which is a GenericsAPI.boolean
	failed_constraint has a value which is a reference to a hash where the key is a string and the value is a string
boolean is an int


=end text

=item Description

validate_data: validate data

=back

=cut

 sub validate_data
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function validate_data (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to validate_data:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'validate_data');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "GenericsAPI.validate_data",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'validate_data',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method validate_data",
					    status_line => $self->{client}->status_line,
					    method_name => 'validate_data',
				       );
    }
}
 


=head2 import_matrix_from_excel

  $returnVal = $obj->import_matrix_from_excel($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a GenericsAPI.ImportMatrixParams
$returnVal is a GenericsAPI.ImportMatrixOutput
ImportMatrixParams is a reference to a hash where the following keys are defined:
	obj_type has a value which is a string
	input_shock_id has a value which is a string
	input_file_path has a value which is a string
	input_staging_file_path has a value which is a string
	matrix_name has a value which is a string
	workspace_name has a value which is a GenericsAPI.workspace_name
	genome_ref has a value which is a GenericsAPI.obj_ref
	col_conditionset_ref has a value which is a GenericsAPI.obj_ref
	row_conditionset_ref has a value which is a GenericsAPI.obj_ref
	diff_expr_matrix_ref has a value which is a GenericsAPI.obj_ref
workspace_name is a string
obj_ref is a string
ImportMatrixOutput is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string
	matrix_obj_ref has a value which is a GenericsAPI.obj_ref

</pre>

=end html

=begin text

$params is a GenericsAPI.ImportMatrixParams
$returnVal is a GenericsAPI.ImportMatrixOutput
ImportMatrixParams is a reference to a hash where the following keys are defined:
	obj_type has a value which is a string
	input_shock_id has a value which is a string
	input_file_path has a value which is a string
	input_staging_file_path has a value which is a string
	matrix_name has a value which is a string
	workspace_name has a value which is a GenericsAPI.workspace_name
	genome_ref has a value which is a GenericsAPI.obj_ref
	col_conditionset_ref has a value which is a GenericsAPI.obj_ref
	row_conditionset_ref has a value which is a GenericsAPI.obj_ref
	diff_expr_matrix_ref has a value which is a GenericsAPI.obj_ref
workspace_name is a string
obj_ref is a string
ImportMatrixOutput is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string
	matrix_obj_ref has a value which is a GenericsAPI.obj_ref


=end text

=item Description

import_matrix_from_excel: import matrix object from excel

=back

=cut

 sub import_matrix_from_excel
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function import_matrix_from_excel (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to import_matrix_from_excel:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'import_matrix_from_excel');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "GenericsAPI.import_matrix_from_excel",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'import_matrix_from_excel',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method import_matrix_from_excel",
					    status_line => $self->{client}->status_line,
					    method_name => 'import_matrix_from_excel',
				       );
    }
}
 


=head2 save_object

  $returnVal = $obj->save_object($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a GenericsAPI.SaveObjectParams
$returnVal is a GenericsAPI.SaveObjectOutput
SaveObjectParams is a reference to a hash where the following keys are defined:
	obj_type has a value which is a string
	obj_name has a value which is a string
	data has a value which is a reference to a hash where the key is a string and the value is a string
	workspace_name has a value which is a GenericsAPI.workspace_name
workspace_name is a string
SaveObjectOutput is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a GenericsAPI.obj_ref
obj_ref is a string

</pre>

=end html

=begin text

$params is a GenericsAPI.SaveObjectParams
$returnVal is a GenericsAPI.SaveObjectOutput
SaveObjectParams is a reference to a hash where the following keys are defined:
	obj_type has a value which is a string
	obj_name has a value which is a string
	data has a value which is a reference to a hash where the key is a string and the value is a string
	workspace_name has a value which is a GenericsAPI.workspace_name
workspace_name is a string
SaveObjectOutput is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a GenericsAPI.obj_ref
obj_ref is a string


=end text

=item Description

save_object: validate data constraints and save matrix object

=back

=cut

 sub save_object
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function save_object (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to save_object:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'save_object');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "GenericsAPI.save_object",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'save_object',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method save_object",
					    status_line => $self->{client}->status_line,
					    method_name => 'save_object',
				       );
    }
}
 


=head2 matrix_filter

  $returnVal = $obj->matrix_filter($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a GenericsAPI.MatrixFilterParams
$returnVal is a GenericsAPI.MatrixFilterOutput
MatrixFilterParams is a reference to a hash where the following keys are defined:
	matrix_obj_ref has a value which is a GenericsAPI.obj_ref
obj_ref is a string
MatrixFilterOutput is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a GenericsAPI.MatrixFilterParams
$returnVal is a GenericsAPI.MatrixFilterOutput
MatrixFilterParams is a reference to a hash where the following keys are defined:
	matrix_obj_ref has a value which is a GenericsAPI.obj_ref
obj_ref is a string
MatrixFilterOutput is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description

matrix_filter: generate a HTML report that allows users to fitler feature ids

=back

=cut

 sub matrix_filter
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function matrix_filter (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to matrix_filter:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'matrix_filter');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "GenericsAPI.matrix_filter",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'matrix_filter',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method matrix_filter",
					    status_line => $self->{client}->status_line,
					    method_name => 'matrix_filter',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "GenericsAPI.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "GenericsAPI.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'matrix_filter',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method matrix_filter",
            status_line => $self->{client}->status_line,
            method_name => 'matrix_filter',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for GenericsAPI::GenericsAPIClient\n";
    }
    if ($sMajor == 0) {
        warn "GenericsAPI::GenericsAPIClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 boolean

=over 4



=item Description

A boolean - 0 for false, 1 for true.
@range (0, 1)


=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 obj_ref

=over 4



=item Description

An X/Y/Z style reference


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 workspace_name

=over 4



=item Description

workspace name of the object


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 FetchDataParams

=over 4



=item Description

Input of the fetch_data function
obj_ref: generics object reference

Optional arguments:
generics_module: the generics data module to be retrieved from
                e.g. for an given data type like below:
                typedef structure {
                  FloatMatrix2D data;
                  condition_set_ref condition_set_ref;
                } SomeGenericsMatrix;
                generics_module should be
                {'data': 'FloatMatrix2D',
                 'condition_set_ref': 'condition_set_ref'}


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
obj_ref has a value which is a GenericsAPI.obj_ref
generics_module has a value which is a reference to a hash where the key is a string and the value is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
obj_ref has a value which is a GenericsAPI.obj_ref
generics_module has a value which is a reference to a hash where the key is a string and the value is a string


=end text

=back



=head2 FetchDataReturn

=over 4



=item Description

Ouput of the fetch_data function
data_matrix: a pandas dataframe in json format


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
data_matrix has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
data_matrix has a value which is a string


=end text

=back



=head2 GenMatrixHTMLParams

=over 4



=item Description

Input of the generate_matrix_html function
df: a pandas dataframe


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
df has a value which is a reference to a hash where the key is a string and the value is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
df has a value which is a reference to a hash where the key is a string and the value is a string


=end text

=back



=head2 GenMatrixHTMLReturn

=over 4



=item Description

Ouput of the generate_matrix_html function
html_string: html as a string format


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
html_string has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
html_string has a value which is a string


=end text

=back



=head2 ExportParams

=over 4



=item Description

Input of the export_matrix function
obj_ref: generics object reference

Optional arguments:
generics_module: select the generics data to be retrieved from
                    e.g. for an given data type like below:
                    typedef structure {
                      FloatMatrix2D data;
                      condition_set_ref condition_set_ref;
                    } SomeGenericsMatrix;
                    and only 'FloatMatrix2D' is needed
                    generics_module should be
                    {'data': FloatMatrix2D'}


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
obj_ref has a value which is a GenericsAPI.obj_ref
generics_module has a value which is a reference to a hash where the key is a string and the value is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
obj_ref has a value which is a GenericsAPI.obj_ref
generics_module has a value which is a reference to a hash where the key is a string and the value is a string


=end text

=back



=head2 ExportOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
shock_id has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
shock_id has a value which is a string


=end text

=back



=head2 ValidateParams

=over 4



=item Description

Input of the validate_data function
obj_type: obj type e.g.: 'KBaseMatrices.ExpressionMatrix-1.1'
data: data to be validated


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
obj_type has a value which is a string
data has a value which is a reference to a hash where the key is a string and the value is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
obj_type has a value which is a string
data has a value which is a reference to a hash where the key is a string and the value is a string


=end text

=back



=head2 ValidateOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
validated has a value which is a GenericsAPI.boolean
failed_constraint has a value which is a reference to a hash where the key is a string and the value is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
validated has a value which is a GenericsAPI.boolean
failed_constraint has a value which is a reference to a hash where the key is a string and the value is a string


=end text

=back



=head2 ImportMatrixParams

=over 4



=item Description

Input of the import_matrix_from_excel function
obj_type: one of ExpressionMatrix, FitnessMatrix, DifferentialExpressionMatrix
input_shock_id: file shock id
input_file_path: absolute file path
input_staging_file_path: staging area file path
matrix_name: matrix object name
workspace_name: workspace name matrix object to be saved to

optional:
col_conditionset_ref: column ConditionSet reference
row_conditionset_ref: row ConditionSet reference
genome_ref: genome reference
diff_expr_matrix_ref: DifferentialExpressionMatrix reference


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
obj_type has a value which is a string
input_shock_id has a value which is a string
input_file_path has a value which is a string
input_staging_file_path has a value which is a string
matrix_name has a value which is a string
workspace_name has a value which is a GenericsAPI.workspace_name
genome_ref has a value which is a GenericsAPI.obj_ref
col_conditionset_ref has a value which is a GenericsAPI.obj_ref
row_conditionset_ref has a value which is a GenericsAPI.obj_ref
diff_expr_matrix_ref has a value which is a GenericsAPI.obj_ref

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
obj_type has a value which is a string
input_shock_id has a value which is a string
input_file_path has a value which is a string
input_staging_file_path has a value which is a string
matrix_name has a value which is a string
workspace_name has a value which is a GenericsAPI.workspace_name
genome_ref has a value which is a GenericsAPI.obj_ref
col_conditionset_ref has a value which is a GenericsAPI.obj_ref
row_conditionset_ref has a value which is a GenericsAPI.obj_ref
diff_expr_matrix_ref has a value which is a GenericsAPI.obj_ref


=end text

=back



=head2 ImportMatrixOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string
matrix_obj_ref has a value which is a GenericsAPI.obj_ref

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string
matrix_obj_ref has a value which is a GenericsAPI.obj_ref


=end text

=back



=head2 SaveObjectParams

=over 4



=item Description

Input of the import_matrix_from_excel function
obj_type: saving object data type
obj_name: saving object name
data: data to be saved
workspace_name: workspace name matrix object to be saved to


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
obj_type has a value which is a string
obj_name has a value which is a string
data has a value which is a reference to a hash where the key is a string and the value is a string
workspace_name has a value which is a GenericsAPI.workspace_name

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
obj_type has a value which is a string
obj_name has a value which is a string
data has a value which is a reference to a hash where the key is a string and the value is a string
workspace_name has a value which is a GenericsAPI.workspace_name


=end text

=back



=head2 SaveObjectOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
obj_ref has a value which is a GenericsAPI.obj_ref

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
obj_ref has a value which is a GenericsAPI.obj_ref


=end text

=back



=head2 MatrixFilterParams

=over 4



=item Description

Input of the matrix_filter function
matrix_obj_ref: object reference of a matrix


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
matrix_obj_ref has a value which is a GenericsAPI.obj_ref

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
matrix_obj_ref has a value which is a GenericsAPI.obj_ref


=end text

=back



=head2 MatrixFilterOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=cut

package GenericsAPI::GenericsAPIClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
