/// <reference path="../../Scripts/typings/angularjs/angular.d.ts" />

'use strict';

module PriceModule {
    export class PriceDirective {
        constructor() {
            return this.CreateDirective();
        }
        private CreateDirective(): any {
            return {
                template: ''
                + '<div id="price_area">'
                +   '<table id="price_table">'
                +     '<tbody>'
                +       '<tr>'
                +         '<td>予測価格</td>'
                +         '<td>'
                +           '{{response_howmuch.price | number}}<small>万円</small>'
                +         '</td>'
                +       '</tr>'
                +       '<tr>'
                +         '<td>価格範囲</td>'
                +         '<td>'
                +           '{{response_howmuch.low | number}}<small>万円</small>'
                +             '～'
                +           '{{response_howmuch.high | number}}<small>万円</small>'
                +         '</td>'
                +       '</tr>'
                +     '</tbody>'
                +   '</table>'
                + '</div>'
            }
        }
    }
}

angular.module('myApp').directive('priceDirective', () => new PriceModule.PriceDirective());
