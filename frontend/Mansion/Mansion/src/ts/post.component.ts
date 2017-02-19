/// <reference path="_include.ts" />

declare var AjaxZip3: AjaxZip3Class
declare class AjaxZip3Class {
  onSuccess: any;
  onFailure: any;
  zip2addr(a:string, b:string, c:string, d:string): void;
};

module app {
    /**
     * Reference コンポーネント作成
     */
    export function PostComponentFactory(): ng.IComponentOptions {
        return {
            bindings:
            {
                //コントローラパラメタ
                addr: '='
            },
            template: [
              '<table id="mansion_info">',
              '<tbody>',
              '<tr>',
              '<td></td>',
              '<td>郵便番号(7桁)</td>',
              '<td>',
              '<input type="number" name="zip11" ng-model="_my.zip_addr.zip" size="9" maxlength="8">',
              '<button ng-click="_my.clickSearchAddress()">郵便番号から住所を入力する</button>',
              '</td>',
              '</tr>',
              '<tr>',
              '<td><div>必須</div></td>',
              '<td>住所</td>',
              '<td>',
              '<input type="text" name="addr11" ng-model="_my.addr" size="60">',
              '</td>',
              '</tr>',
              '<tr>',
              '<td><div>必須</div></td>',
              '<td>築年数</td>',
              '<td><input type="number" id="year" ng-model="_my.year" size="4"></td>',
              '</tr>',
              '<tr>',
              '<td><div>必須</div></td>',
              '<td>占有面積(㎡)</td>',
              '<td><input type="number" id="occupied" ng-model="_my.occupied" size="4"></td>',
              '</tr>',
              '<tr>',
              '<td><div>必須</div></td>',
              '<td>駅まで徒歩(分)</td>',
              '<td><input type="number" id="walk" ng-model="_my.walk" size="4"></td>',
              '</tr>',
              '</tbody>',
              '</table>',
            ].join(""),
            controllerAs: '_my',
            controller: PostComponent
        };
    }

    /**
     * コントローラ
     * @returns
     */
    class PostComponent {
        public static $inject = ['toastr'];  // httpサービスの注入
        zip_addr: any;
        addr: string;
        PREFLIST: string[];
        _toastr: any;

        /**
         * コンストラクタ
         * @param {ng.resource.IResourceService} public $resource
         */
        constructor(public toastr: any) {
          this.PREFLIST = [
              '埼玉県', '千葉県', '東京都', '神奈川県'
          ]
          var zip_addr = {
            zip: '',
            addr: ''
          };
          this._toastr = toastr;
          this.zip_addr = zip_addr;
          var that = this;

          AjaxZip3.onSuccess = function () {
              if (!checkPrefecture()) {
                  that.addr = ""
                  toastr.error('予想可能な都道府県を指定してください', '郵便番号エラー');
                  return
              }
              //angular.element(
              //    (<HTMLInputElement>document.getElementsByName('addr11')[0])
              //).triggerHandler('input')
          }
          AjaxZip3.onFailure = function () {
              toastr.error('郵便番号に該当する住所を取得できません。', '郵便番号エラー');
          }

          function checkPrefecture() {
              var address = (<HTMLInputElement>document.getElementsByName('addr11')[0]).value
              for (var pref of that.PREFLIST) {
                  if (address.lastIndexOf(pref, 0) == 0) {
                      return true
                  }
              }
              return false
          }
        }

        clickSearchAddress() {
            if (('' + this.zip_addr.zip).length == 7) {
                AjaxZip3.zip2addr('zip11', '', 'addr11', 'addr11')
            } else {
                this._toastr.error('7桁の数値を指定してください', '郵便番号エラー');
            }
        };
    }
}
