/// <reference path="_include.ts" />
module app {
    /**
     * Error コンポーネント作成
     */
    export function ErrorComponentFactory(): ng.IComponentOptions {
        return {
            bindings:
            {
                //コントローラパラメタ
                paramTitle: '='
            },
            template: [
                '<table id="error_rate">',
                '<thead>',
                '<tr><th>誤差率</th><th>件数</th><th>割合</th></tr>',
                '</thead>',
                '<tbody>',
                '<tr ng-repeat="error in _my.errorList">',
                '<td>{{error.class}}</td>',
                '<td>{{error.count | number}}</td>',
                '<td>{{error.percentage}}</td>',
                '</tr>',
                '</tbody>',
                '</table>'
            ].join(""),
            controllerAs: '_my',
            controller: ErrorComponent
        };
    }

    /**
     * コントローラ
     * @returns
     */
    class ErrorComponent {
        /**
         * 表示項目
         */
        errorList: Array<any>;

        /**
         * コンストラクタ
         */
        constructor() {
            this.errorList = [
                {
                    class: '10%未満',
                    count: 3407,
                    percentage: '14%'
                },
                {
                    class: '20%未満',
                    count: 7045,
                    percentage: '30%'
                },
                {
                    class: '30%未満',
                    count: 10816,
                    percentage: '46%'
                },
                {
                    class: '40%未満',
                    count: 14522,
                    percentage: '62%'
                },
                {
                    class: '50%未満',
                    count: 17825,
                    percentage: '77%'
                },
                {
                    class: '60%未満',
                    count: 19954,
                    percentage: '86%'
                },
                {
                    class: '70%未満',
                    count: 21115,
                    percentage: '91%'
                }
            ]
        }
    }
}
