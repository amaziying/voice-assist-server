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
        newList.map(item => {
            if (item.status === 'OPEN') {
                item.prettyStatus = 'OPEN SINCE ' + moment(item.ts_request).format('h:mm A')
            } else if (item.status === 'INPROGRESS') {
                item.prettyStatus = 'IN PROGRESS SINCE ' + moment(item.ts_pickup).format('h:mm A')
            }
            if (!item.name) {
                item.name = item.patient_id;
            }
            return item;
        })
        $scope.requests = newList;
    });
}]);