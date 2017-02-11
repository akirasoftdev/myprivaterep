var ErrorModule;
(function (ErrorModule) {
    var ErrorController = (function () {
        function ErrorController($scope, ErrorList) {
            this.$scope = $scope;
            $scope.error_list = ErrorList();
        }
        ErrorController.$inject = ['$scope', 'ErrorList'];
        return ErrorController;
    }());
    ErrorModule.ErrorController = ErrorController;
})(ErrorModule || (ErrorModule = {}));
angular.module('myApp').controller('ErrorCtrl', ErrorModule.ErrorController);
var PredictionModule;
(function (PredictionModule) {
    var PredictionController = (function () {
        function PredictionController($scope, predictionService) {
            this.$scope = $scope;
            this.sthis = this;
            $scope.clickPrediction = function () {
                var address = $scope.main.addr;
                var year = $scope.main.year;
                var occupied = $scope.main.occupied;
                var walk = $scope.main.walk;
                var aa = predictionService.get(address, year, occupied, walk);
                aa.then(function (obj) {
                    $scope.response_howmuch = obj;
                }, function () {
                    console.log('error');
                });
            };
        }
        PredictionController.$inject = ['$scope', 'predictionService'];
        return PredictionController;
    }());
    PredictionModule.PredictionController = PredictionController;
})(PredictionModule || (PredictionModule = {}));
angular.module('myApp').controller('PredictionCtrl', PredictionModule.PredictionController);
'use strict';
var ErrorModule;
(function (ErrorModule) {
    var ErrorDirective = (function () {
        function ErrorDirective() {
            return this.CreateDirective();
        }
        ErrorDirective.prototype.CreateDirective = function () {
            return {
                template: ''
                    + '<table id="error_rate">'
                    + '<thead>'
                    + '<tr><th>誤差率</th><th>件数</th><th>割合</th></tr>'
                    + '</thead>'
                    + '<tbody>'
                    + '<tr ng-repeat="error in error_list">'
                    + '<td>{{error.class}}</td>'
                    + '<td>{{error.count | number}}</td>'
                    + '<td>{{error.percentage}}</td>'
                    + '</tr>'
                    + '</tbody>'
                    + '</table>'
            };
        };
        return ErrorDirective;
    }());
    ErrorModule.ErrorDirective = ErrorDirective;
})(ErrorModule || (ErrorModule = {}));
angular.module('myApp').directive('errorDirective', function () { return new ErrorModule.ErrorDirective(); });
'use strict';
var PriceModule;
(function (PriceModule) {
    var PriceDirective = (function () {
        function PriceDirective() {
            return this.CreateDirective();
        }
        PriceDirective.prototype.CreateDirective = function () {
            return {
                template: ''
                    + '<div id="price_area">'
                    + '<table id="price_table">'
                    + '<tbody>'
                    + '<tr>'
                    + '<td>予測価格</td>'
                    + '<td>'
                    + '{{response_howmuch.price | number}}<small>万円</small>'
                    + '</td>'
                    + '</tr>'
                    + '<tr>'
                    + '<td>価格範囲</td>'
                    + '<td>'
                    + '{{response_howmuch.low | number}}<small>万円</small>'
                    + '～'
                    + '{{response_howmuch.high | number}}<small>万円</small>'
                    + '</td>'
                    + '</tr>'
                    + '</tbody>'
                    + '</table>'
                    + '</div>'
            };
        };
        return PriceDirective;
    }());
    PriceModule.PriceDirective = PriceDirective;
})(PriceModule || (PriceModule = {}));
angular.module('myApp').directive('priceDirective', function () { return new PriceModule.PriceDirective(); });
'use strict';
var ReferenceModule;
(function (ReferenceModule) {
    var ReferenceDirective = (function () {
        function ReferenceDirective() {
            return this.CreateDirective();
        }
        ReferenceDirective.prototype.CreateDirective = function () {
            return {
                template: ''
                    + '<table id="references">'
                    + '<thead>'
                    + '<tr>'
                    + '<th>住所</th>'
                    + '<th>築年</th>'
                    + '<th>面積(㎡)</th>'
                    + '<th>駅</th>'
                    + '<th>徒歩(分)</th>'
                    + '<th>掲載金額(万円)</th>'
                    + '</tr>'
                    + '</thead>'
                    + '<tbody>'
                    + '<tr ng-repeat="ref in response_howmuch.ref">'
                    + '<td>{{ref.address}}</td>'
                    + '<td>{{ref.year}}</td>'
                    + '<td>{{ref.occupiedArea}}</td>'
                    + '<td>{{ref.station}}</td>'
                    + '<td>{{ref.walkTime}}</td>'
                    + '<td>{{ref.price | number}}</td>'
                    + '</tr>'
                    + '</tbody>'
                    + '</table>'
            };
        };
        return ReferenceDirective;
    }());
    ReferenceModule.ReferenceDirective = ReferenceDirective;
})(ReferenceModule || (ReferenceModule = {}));
angular.module('myApp').directive('referenceDirective', function () { return new ReferenceModule.ReferenceDirective(); });
'use strict';
var PredictionModule;
(function (PredictionModule) {
    var PredictionService = (function () {
        function PredictionService($q, $http) {
            this.$q = $q;
            this.$http = $http;
            this.q = $q;
            this.http = $http;
        }
        PredictionService.prototype.get = function (address, year, occupied, walk) {
            var d = this.q.defer();
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
                var json = JSON.parse(data);
                d.resolve(json);
            })
                .error(function (data, status, headers, config) {
                d.reject();
            });
            return d.promise;
        };
        return PredictionService;
    }());
    PredictionModule.PredictionService = PredictionService;
})(PredictionModule || (PredictionModule = {}));
angular.module('myApp').service('predictionService', PredictionModule.PredictionService);
'use strict';
var ZipAddrModule;
(function (ZipAddrModule) {
    var ZipAddrService = (function () {
        function ZipAddrService($q) {
            this.$q = $q;
            this.PREFLIST = [
                '埼玉県', '千葉県', '東京都', '神奈川県'
            ];
            this.q = $q;
        }
        ZipAddrService.prototype.get = function (element_name) {
            var d = this.q.defer();
            AjaxZip3.onSuccess = function () {
                var address = document.getElementsByName(element_name)[0];
                if (!this.checkPrefecture(address)) {
                    address.value = "";
                    toastr.error('予想可能な都道府県を指定してください', '郵便番号エラー');
                    d.reject();
                    return;
                }
                angular.element(address).triggerHandler('input');
            };
            AjaxZip3.onFailure = function () {
                this.toastr.error('郵便番号に該当する住所を取得できません。', '郵便番号エラー');
            };
        };
        ZipAddrService.prototype.checkPrefecture = function (address) {
            for (var _i = 0, _a = this.PREFLIST; _i < _a.length; _i++) {
                var pref = _a[_i];
                if (address.value.startsWith(pref)) {
                    return true;
                }
            }
            return false;
        };
        ZipAddrService.$inject = ['toastr'];
        return ZipAddrService;
    }());
    ZipAddrModule.ZipAddrService = ZipAddrService;
})(ZipAddrModule || (ZipAddrModule = {}));
angular.module('myApp').service('zipAddrService', ZipAddrModule.ZipAddrService);
