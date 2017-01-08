module PredictionModule {
    export class PredictionController {
        static $inject = ['$scope', 'predictionService'];
        private sthis;

        constructor(private $scope, predictionService) {
            this.sthis = this
            $scope.clickPrediction = function() {
                var address = $scope.main.addr;
                var year = $scope.main.year;
                var occupied = $scope.main.occupied;
                var walk = $scope.main.walk;
                var aa = predictionService.get(address, year, occupied, walk)
                aa.then(function(obj) {
                    $scope.response_howmuch = obj
                }, function() {
                    console.log('error')
                })
            }
        }
    }
}

angular.module('myApp').controller('PredictionCtrl', PredictionModule.PredictionController)