app.controller('mainController', ['$scope', 'requestService', function ($scope, requestService) {
	$scope.requests = [];

	$scope.requestAction = function (id) {
		const request = $scope.requests.find(r => r.id === id);
		if (!request) return;

		if (request.status === 'OPEN') {
			requestService.pickup(id);
		} else if (request.status === 'INPROGRESS') {
			requestService.close(id);
		}
	};

	requestService.subscribe(function (newList) {
		$scope.requests = newList;
	});
}]);