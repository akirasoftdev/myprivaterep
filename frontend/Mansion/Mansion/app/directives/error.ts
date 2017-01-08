/// <reference path="../../Scripts/typings/angularjs/angular.d.ts" />

'use strict';

module ErrorModule {
    export class ErrorDirective {
        constructor() {
            return this.CreateDirective();
        }
        private CreateDirective(): any {
            return {
                template: ''
	            + '<table id="error_rate">'
	            +   '<thead>'
	            +     '<tr><th>誤差率</th><th>件数</th><th>割合</th></tr>'
	            +   '</thead>'
	            +   '<tbody>'
	            +     '<tr ng-repeat="error in error_list">'
	            +       '<td>{{error.class}}</td>'
	            +       '<td>{{error.count | number}}</td>'
	            +       '<td>{{error.percentage}}</td>'
	            +     '</tr>'
	            +   '</tbody>'
                + '</table>'
            }
        }
    }
}

angular.module('myApp').directive('errorDirective', () => new ErrorModule.ErrorDirective());
