/// <reference path="_include.ts" />
module app {
    /**
     * Reference コンポーネント作成
     */
    export function ReferenceComponentFactory(): ng.IComponentOptions {
        return {
            bindings:
            {
                //コントローラパラメタ
                paramTitle: '='
            },
            template: [
                    '<table id="references">',
                    '<thead>',
                    '<tr><th>住所</th><th>築年</th><th>面積(㎡)</th><th>駅</th><th>徒歩(分)</th><th>掲載金額(万円)</th></tr>',
                    '</thead>',
                    '<tbody>',
                    '<tr ng-repeat="ref in _my.responseHowMuch">',
                    '<td>{{ref.address}}</td>',
                    '<td>{{ref.year}}</td>',
                    '<td>{{ref.occupiedArea}}</td>',
                    '<td>{{ref.station}}</td>',
                    '<td>{{ref.walkTime}}</td>',
                    '<td>{{ref.price}}</td>',
                    '</tbody>',
                    '</table>'
                ].join(""),
            controllerAs: '_my',
            controller: ReferenceComponent
        };
    }

    interface BukkenObject {
        address: string;
        price: number;
        year: number;
        occupiedArea: number;
        station: number;
        walkTime: number;
    }

    interface PredictionObject {
        price: number;
        low: number;
        high: number;
        ref: BukkenObject[];
    }

    /**
     * コントローラ
     * @returns
     */
    class ReferenceComponent {
        public static $inject = ['$resource'];  // httpサービスの注入
        responseHowMuch = [];
        hostName = 'http://mansion-prediction-dev.5grvpjfmbg.ap-northeast-1.elasticbeanstalk.com';
        address = '東京都品川区西五反田';
        year = 11;
        occupied = 100;
        walk = 10;

        /**
         * コンストラクタ
         * @param {ng.resource.IResourceService} public $resource
         */
        constructor(public $resource: ng.resource.IResourceService) {
            var that = this

            var resourceHowMuch = $resource<PredictionObject>(this.hostName + '/howmuch', {
                address: this.address,
                year: this.year,
                occupied: this.occupied,
                walk: this.walk
            }, {query: {method:'GET', isArray:false}})

            var response = resourceHowMuch.query(function() {
                console.log(response)
                that.to_reference(response)
            }, function() {
                console.log('ERROR')
            })
        }

        public to_reference(response) {
            var that = this
            response['ref'].forEach(function(bukken) {
                that.responseHowMuch.push({
                    address: bukken['address'],
                    year: bukken['year'],
                    occupiedArea: bukken['occupiedArea'] / 100,
                    station: bukken['station'],
                    walkTime: bukken['walkTime'],
                    price: bukken['price'].toLocaleString()
                })
            })
        }
    }
}
