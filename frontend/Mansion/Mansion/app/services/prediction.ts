'use strict'

module PredictionModule {
    export class PredictionService {
        private q: ng.IQService;
        private http;
        constructor(private $q: ng.IQService, private $http) {
            this.q = $q;
            this.http = $http;
        }

        get(address, year, occupied, walk): ng.IPromise<any> {
            var d = this.q.defer<any>();
            this.http({
                method: 'GET',
                url: 'howmuch',
                params: {
                    address: address,
                    year: year,
                    occupied: occupied,
                    walk: walk
                }
            })
                .success(function (data, status, headers, config) {
                    var json = JSON.parse(data)
                    d.resolve(json)
                })
                .error(function (data, status, headers, config) {
                    d.reject()
                });
            return d.promise;
        }
    }
}

angular.module('myApp').service('predictionService', PredictionModule.PredictionService);
