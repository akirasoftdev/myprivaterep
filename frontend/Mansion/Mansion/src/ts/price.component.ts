/// <reference path="_include.ts" />
module app {
    /**
     * Price コンポーネント作成
     */
    export function PriceComponentFactory(): ng.IComponentOptions {
        return {
            bindings:
            {
                //コントローラパラメタ
                paramTitle: '=',
                //コールバック
                callBackEvent: '&'
            },
            template: [
                    '<div id="price_area">',
                    '<table id="price_table">',
                    '<tbody>',
                    '<tr>',
                    '<td>予測価格</td>',
                    '<td>{{_my.price | number}}<small>万円</small></td>',
                    '</tr>',
                    '<tr>',
                    '<td>価格範囲</td>',
                    '<td>',
                    '{{_my.low | number}}<small>万円</small>',
                    '～',
                    '{{_my.high | number}}<small>万円</small>',
                    '</td>',
                    '</tr>',
                    '</tbody>',
                    '</table>',
                    '</div>'
                ].join(""),
            controllerAs: '_my',
            controller: PriceComponent
        };
    }
    /**
     * コントローラ
     * @returns
     */
    class PriceComponent {
        public static $inject = ['$http'];  // httpサービスの注入
        hostName = 'http://mansion-prediction-dev.5grvpjfmbg.ap-northeast-1.elasticbeanstalk.com';
        address = '千葉県市川市新田';
        year = 11;
        occupied = 100;
        walk = 10;
        /**
         * 表示項目
         */
        price: number;
        low: number;
        high: number;

        /**
         * コンストラクタ
         * @param {ng.IHttpService} public $http
         */
        constructor(public $http: ng.IHttpService) {
            var that = this

            // this.$http で httpサービスが使用可能
            this.$http({
                method: 'GET',
                url: this.hostName + '/howmuch?address=' + this.address + '&year=' + this.year + '&occupied=' + this.occupied + '&walk=' + this.walk,
            })
            .then(
                function onSuccess(response) {
                    console.log(response)
                    var json = response.data
                    that.price = json['price']
                    that.low = json['low']
                    that.high = json['high']
                },
                function onError(response) {
                    console.log(response)
                }
            )
        }
    }
}
