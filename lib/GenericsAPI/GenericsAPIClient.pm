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
	workspace_name has a value which is a string
	target_data_field has a value which is a string
obj_ref is a string
FetchDataReturn is a reference to a hash where the following keys are defined:
	data_matrix has a value which is a reference to a hash where the key is a string and the value is a string

</pre>

=end html

=begin text

$params is a GenericsAPI.FetchDataParams
$returnVal is a GenericsAPI.FetchDataReturn
FetchDataParams is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a GenericsAPI.obj_ref
	workspace_name has a value which is a string
	target_data_field has a value which is a string
obj_ref is a string
FetchDataReturn is a reference to a hash where the following keys are defined:
	data_matrix has a value which is a reference to a hash where the key is a string and the value is a string


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
	data_matrix has a value which is a reference to a hash where the key is a string and the value is a string
GenMatrixHTMLReturn is a reference to a hash where the following keys are defined:
	html_string has a value which is a string

</pre>

=end html

=begin text

$params is a GenericsAPI.GenMatrixHTMLParams
$returnVal is a GenericsAPI.GenMatrixHTMLReturn
GenMatrixHTMLParams is a reference to a hash where the following keys are defined:
	data_matrix has a value which is a reference to a hash where the key is a string and the value is a string
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
                method_name => 'generate_matrix_html',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method generate_matrix_html",
            status_line => $self->{client}->status_line,
            method_name => 'generate_matrix_html',
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



=head2 FetchDataParams

=over 4



=item Description

Input of the fetch_data function
obj_ref: generics object reference
workspace_name: the name of the workspace

Optional arguments:
target_data_field: the data field to be retrieved from.
                   fetch_data will try to auto find this field.
                    e.g. for an given data type like below:
                    typedef structure {
                      FloatMatrix2D data;
                    } SomeGenericsMatrix;
                    data should be the target data field.


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
obj_ref has a value which is a GenericsAPI.obj_ref
workspace_name has a value which is a string
target_data_field has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
obj_ref has a value which is a GenericsAPI.obj_ref
workspace_name has a value which is a string
target_data_field has a value which is a string


=end text

=back



=head2 FetchDataReturn

=over 4



=item Description

Ouput of the fetch_data function
data_matrix: a pandas dataframe


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
data_matrix has a value which is a reference to a hash where the key is a string and the value is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
data_matrix has a value which is a reference to a hash where the key is a string and the value is a string


=end text

=back



=head2 GenMatrixHTMLParams

=over 4



=item Description

Input of the generate_matrix_html function
data_matrix: a pandas dataframe
        e.g. {'Department': 'string', 'Revenues':'number'}
data: data used to generate html report
      e.g. [['Shoes', 10700], ['Sports', -15400]]


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
data_matrix has a value which is a reference to a hash where the key is a string and the value is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
data_matrix has a value which is a reference to a hash where the key is a string and the value is a string


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
