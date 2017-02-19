(function () {

    angular.module('app')
    .controller('PredictionCtrl', function ($scope, $http) {
        sthis = this
        $scope.clickPrediction = function () {
            $http({
                method: 'GET',
                url: 'howmuch',
                params: {
                    address: sthis.addr,
                    year: sthis.year,
                    occupied: sthis.occupied,
                    walk: sthis.walk
                }
            })
            .success(function (data, status, headers, config) {
                var json = JSON.parse(data)
                sthis.price = json['price']
                sthis.price_low = json['low']
                sthis.price_high = json['high']
                sthis.references = json['ref']
            })
            .error(function (data, status, headers, config) {
                console.log("")
            });
        }
    })


})();
