app.factory('requestService', ['$http', '$timeout', function ($http, $timeout) {
	const subscriptions = [];
	let str = '';

	function notifySubscribers(requests) {
		subscriptions.forEach(cb => cb(requests));
	}

	function poll() {
		$http.get('/api/requests?finder=active').then(function (response) {
			const resultStr = angular.toJson(response.data.result);
			if (str !== resultStr) {
				str = resultStr;
				notifySubscribers(response.data.result);
			}
		}, function (err) {
			console.log(err);
		});
		$timeout(poll, 500);
	}
	poll();

	return {
		subscribe: function (cb) {
			subscriptions.push(cb);
		},
		pickup: function (id) {
			return $http.post('/api/pickup_request', {'request_id': id});
		},
		close: function (id) {
			return $http.post('/api/close_request', {'request_id': id});
		}
	};
}]);