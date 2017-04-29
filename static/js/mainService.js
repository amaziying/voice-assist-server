app.factory('requestService', ['$http', function ($http) {
	return {
		fetch: function () {
			return $http.get('/api/requests?finder=active');
		},
		pickup: function (id) {
			return $http.post('/api/pickup_request', {'request_id': id});
		},
		close: function (id) {
			return $http.post('/api/close_request', {'request_id': id});
		}
	};
}]);