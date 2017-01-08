(function () {

    var myApp = angular.module('myApp');
    var PREFLIST = [
        '埼玉県', '千葉県', '東京都', '神奈川県'
    ]

    myApp.controller('InParamCtrl', ['$scope', 'toastr', 'zipAddrService', function ($scope, toastr, zipAddrService) {
        var zip_addr = {};
        zip_addr.zip = "";
        zip_addr.addr = "";
        $scope.zip_addr = zip_addr;
        zipAddrService.get('addr11')

        AjaxZip3.onSuccess = function () {
            var address = document.getElementsByName('addr11')[0]
            if (!checkPrefecture(address)) {
                $scope.main.addr = ""
                address.value = ""
                toastr.error('予想可能な都道府県を指定してください', '郵便番号エラー');
                return
            }
            angular.element(address).triggerHandler('input')
        }
        AjaxZip3.onFailure = function () {
            toastr.error('郵便番号に該当する住所を取得できません。', '郵便番号エラー');
        }

        function checkPrefecture(address) {
            for (var pref of PREFLIST) {
                if (address.value.startsWith(pref)) {
                    return true
                }
            }
            return false
        }

        $scope.clickSearchAddress = function () {
            if (('' + this.zip_addr.zip).length == 7) {
                AjaxZip3.zip2addr('zip11', '', 'addr11', 'addr11')
            } else {
                toastr.error('7桁の数値を指定してください', '郵便番号エラー');
            }
        };
    }]);

})();
