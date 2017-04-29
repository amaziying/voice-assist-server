app.controller('mainController', ['$scope', '$timeout', 'requestService', function ($scope, $timeout, requests) {
	$scope.requests = [];

	function poll() {
		requests.fetch().then(function (response) {
			$scope.requests = response.data.result;
		}, function (err) {
			console.log(err);
		});
		$timeout(poll, 1000);
	}
	poll();
}]);