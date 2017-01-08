'use strict'

module ZipAddrModule {
    export class ZipAddrService {
        static $inject = ['toastr'];
        private PREFLIST = [
            '埼玉県', '千葉県', '東京都', '神奈川県'
        ]
        private q: ng.IQService;

        constructor(private $q) {
            this.q = $q;
        }

        public get(element_name) {
            var d = this.q.defer<any>();
            AjaxZip3.onSuccess = function () {
                var address = document.getElementsByName(element_name)[0]
                if (!this.checkPrefecture(address)) {
                    address.value = ""
                    toastr.error('予想可能な都道府県を指定してください', '郵便番号エラー');
                    d.reject()
                    return
                }
                angular.element(address).triggerHandler('input')
            }
            AjaxZip3.onFailure = function () {
                this.toastr.error('郵便番号に該当する住所を取得できません。', '郵便番号エラー');
            }
        }

        private checkPrefecture(address) {
            for (var pref of this.PREFLIST) {
                if (address.value.startsWith(pref)) {
                    return true
                }
            }
            return false
        }
    }
}

angular.module('myApp').service('zipAddrService', ZipAddrModule.ZipAddrService);