module ErrorModule {
    export class ErrorController {
        static $inject = ['$scope', 'ErrorList'];

        constructor(private $scope, ErrorList) {
            $scope.error_list = ErrorList()
        }
    }
}

angular.module('myApp').controller('ErrorCtrl', ErrorModule.ErrorController)