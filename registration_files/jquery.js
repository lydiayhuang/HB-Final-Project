<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <!--[if IE]><meta http-equiv="X-UA-Compatible" content="IE=edge" /><![endif]-->
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Error</title>
  <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"
        rel="stylesheet">
  <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
  <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
  <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
    <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  <script src="//code.jquery.com/jquery.min.js"></script>
  <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
  <link
      href="//fonts.googleapis.com/css?family=Open+Sans:400,700,400italic,700italic"
      rel="stylesheet">
  <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css"
        rel="stylesheet">
  <style>
    .errorpage-row {
      margin-top: 5em;
    }

    @media (min-width: 768px) {
      .errorpage-row {
        margin-top: 10em;
      }
    }

    body {
      font-family: "Open Sans", sans-serif;
    }

    .error-form {
      margin-bottom: 1.5em;
    }
  </style>
</head>
<body>
<div class="container">
  <div class="errorpage-row row">
    <div class="visible-md visible-lg col-md-5 col-md-offset-1">
      <a href="/">
        <img title="Sad Balloonicorn" src="//temp.joelburton.com/balloonicorn.jpg"
             align="right">
      </a>
    </div>
    <div class="col-md-5 col-sm-6 col-sm-offset-3 col-xs-8 col-xs-offset-2 col-md-offset-0">


      <div class="page-header">
        <h1>Ut oh.</h1>

        <p class="lead">I can&rsquo;t find the page you&rsquo;re looking for.</p>
      </div>

      <p>Start at our <a href="/">home page</a> or use site search:</p>

      <form action="/search">
        <div class="input-group">
          <label for="searchbox" class="sr-only">Search</label>
          <input type="text" class="form-control" placeholder="Search"
                 name="q" accesskey="4">

          <div class="input-group-btn">
            <button class="btn btn-default" type="submit"><i
                class="glyphicon glyphicon-search"><span
                class="sr-only">Search</span></i>
            </button>
          </div>
        </div>
      </form>

      <p>
        If you feel like you reached this message in error, or need help,
        please <a href="mailto:joel@hackbrightacademy.com">email our webmaster</a>.
      </p>

    </div>
  </div>
</div>
</body>
</html>
