Attribute VB_Name = "GenerateCaseNumber"
'
' 案件番号生成モジュール
' Phase 2で実装
'
' 案件番号採番サーバーと通信して、案件番号を取得する
' サーバーが利用できない場合は、ローカルで採番する（フォールバック）
'

Option Explicit

' サーバー設定（config.jsonから取得するか、ここで定義）
Private Const SERVER_HOST As String = "localhost"
Private Const SERVER_PORT As Long = 8080
Private Const SERVER_TIMEOUT As Long = 5 ' 秒
Private Const ENABLE_FALLBACK As Boolean = True

'
' 案件番号をサーバーから取得する
'
' @param caseType 案件種別 (EX, IM, TR, DO)
' @param userName ユーザー名
' @return 案件番号（例: EX-250001）
'
Public Function GenerateCaseNumberFromServer(caseType As String, userName As String) As String
    On Error GoTo ErrorHandler
    
    ' 入力検証
    If caseType = "" Then
        MsgBox "案件種別が指定されていません", vbCritical, "エラー"
        GenerateCaseNumberFromServer = ""
        Exit Function
    End If
    
    If userName = "" Then
        userName = Environ("USERNAME") ' Windowsユーザー名を使用
    End If
    
    ' サーバーから案件番号を取得
    Dim caseNumber As String
    caseNumber = RequestCaseNumber(caseType, userName)
    
    ' 成功した場合は結果を返す
    If caseNumber <> "" Then
        GenerateCaseNumberFromServer = caseNumber
        Exit Function
    End If
    
    ' サーバーが利用できない場合、フォールバックを試みる
    If ENABLE_FALLBACK Then
        MsgBox "サーバーに接続できないため、ローカルで案件番号を生成します。" & vbCrLf & _
               "重複の可能性があるため、後で確認してください。", _
               vbExclamation, "警告"
        
        caseNumber = GenerateCaseNumberLocal(caseType)
        GenerateCaseNumberFromServer = caseNumber
    Else
        MsgBox "サーバーに接続できませんでした。" & vbCrLf & _
               "ネットワーク接続とサーバーの状態を確認してください。", _
               vbCritical, "エラー"
        GenerateCaseNumberFromServer = ""
    End If
    
    Exit Function
    
ErrorHandler:
    MsgBox "案件番号の生成中にエラーが発生しました: " & Err.Description, _
           vbCritical, "エラー"
    GenerateCaseNumberFromServer = ""
End Function

'
' サーバーに案件番号をリクエスト
'
' @param caseType 案件種別
' @param userName ユーザー名
' @return 案件番号（失敗時は空文字列）
'
Private Function RequestCaseNumber(caseType As String, userName As String) As String
    On Error GoTo ErrorHandler
    
    ' URLを構築
    Dim url As String
    url = "http://" & SERVER_HOST & ":" & SERVER_PORT & "/generate" & _
          "?type=" & caseType & "&user=" & UrlEncode(userName)
    
    ' HTTPリクエストを作成
    Dim http As Object
    Set http = CreateObject("MSXML2.XMLHTTP")
    
    ' タイムアウト設定（ミリ秒）
    http.Open "GET", url, False
    http.setTimeouts SERVER_TIMEOUT * 1000, SERVER_TIMEOUT * 1000, _
                     SERVER_TIMEOUT * 1000, SERVER_TIMEOUT * 1000
    
    ' リクエストを送信
    http.send
    
    ' レスポンスを確認
    If http.Status = 200 Then
        ' JSONレスポンスをパース
        Dim response As String
        response = http.responseText
        
        ' 簡易JSONパース（successとcase_numberを抽出）
        Dim caseNumber As String
        caseNumber = ParseCaseNumber(response)
        
        If caseNumber <> "" Then
            RequestCaseNumber = caseNumber
        Else
            RequestCaseNumber = ""
        End If
    Else
        ' HTTPエラー
        Debug.Print "HTTP Error: " & http.Status & " - " & http.statusText
        RequestCaseNumber = ""
    End If
    
    Set http = Nothing
    Exit Function
    
ErrorHandler:
    Debug.Print "RequestCaseNumber Error: " & Err.Description
    RequestCaseNumber = ""
End Function

'
' JSONレスポンスから案件番号を抽出
'
' @param jsonString JSON文字列
' @return 案件番号
'
Private Function ParseCaseNumber(jsonString As String) As String
    On Error Resume Next
    
    ' 簡易的なJSONパース（正規表現を使用）
    Dim regex As Object
    Set regex = CreateObject("VBScript.RegExp")
    
    ' "case_number": "XX-YYZZZZ" の部分を抽出
    regex.Pattern = """case_number""\s*:\s*""([^""]+)"""
    regex.Global = False
    regex.IgnoreCase = True
    
    Dim matches As Object
    Set matches = regex.Execute(jsonString)
    
    If matches.Count > 0 Then
        ParseCaseNumber = matches(0).SubMatches(0)
    Else
        ParseCaseNumber = ""
    End If
    
    Set regex = Nothing
End Function

'
' ローカルで案件番号を生成（フォールバック）
'
' @param caseType 案件種別
' @return 案件番号
'
Private Function GenerateCaseNumberLocal(caseType As String) As String
    On Error Resume Next
    
    ' 現在のシートから最大番号を取得
    Dim ws As Worksheet
    Set ws = ActiveSheet ' または特定のシートを指定
    
    ' 案件番号列を検索（A列と仮定）
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    
    ' 該当種別の最大番号を検索
    Dim maxNumber As Long
    maxNumber = 0
    
    Dim i As Long
    For i = 2 To lastRow ' ヘッダー行をスキップ
        Dim cellValue As String
        cellValue = ws.Cells(i, "A").Value
        
        ' 該当種別の案件番号かチェック
        If Left(cellValue, Len(caseType) + 1) = caseType & "-" Then
            ' 番号部分を抽出（例: EX-250001 → 250001）
            Dim numberPart As String
            numberPart = Mid(cellValue, Len(caseType) + 2)
            
            ' 数値に変換
            Dim num As Long
            num = Val(numberPart)
            
            If num > maxNumber Then
                maxNumber = num
            End If
        End If
    Next i
    
    ' 次の番号を生成
    Dim nextNumber As Long
    nextNumber = maxNumber + 1
    
    ' 年度サフィックス
    Dim yearSuffix As String
    yearSuffix = Format(Now, "yy")
    
    ' 案件番号を生成（例: EX-250001）
    GenerateCaseNumberLocal = caseType & "-" & yearSuffix & Format(nextNumber, "0000")
End Function

'
' URL エンコード
'
' @param text エンコードする文字列
' @return エンコードされた文字列
'
Private Function UrlEncode(text As String) As String
    Dim i As Long
    Dim char As String
    Dim result As String
    
    result = ""
    
    For i = 1 To Len(text)
        char = Mid(text, i, 1)
        
        ' アルファベット、数字、一部の記号はそのまま
        If char Like "[A-Za-z0-9-_.~]" Then
            result = result & char
        Else
            ' それ以外はURLエンコード
            result = result & "%" & Right("0" & Hex(Asc(char)), 2)
        End If
    Next i
    
    UrlEncode = result
End Function

'
' サーバーのヘルスチェック
'
' @return True: サーバーが正常, False: サーバーが異常
'
Public Function CheckServerHealth() As Boolean
    On Error GoTo ErrorHandler
    
    ' URLを構築
    Dim url As String
    url = "http://" & SERVER_HOST & ":" & SERVER_PORT & "/health"
    
    ' HTTPリクエストを作成
    Dim http As Object
    Set http = CreateObject("MSXML2.XMLHTTP")
    
    ' タイムアウト設定
    http.Open "GET", url, False
    http.setTimeouts 2000, 2000, 2000, 2000
    
    ' リクエストを送信
    http.send
    
    ' レスポンスを確認
    If http.Status = 200 Then
        CheckServerHealth = True
    Else
        CheckServerHealth = False
    End If
    
    Set http = Nothing
    Exit Function
    
ErrorHandler:
    CheckServerHealth = False
End Function

'
' サーバーのステータスを表示
'
Public Sub ShowServerStatus()
    On Error Resume Next
    
    ' URLを構築
    Dim url As String
    url = "http://" & SERVER_HOST & ":" & SERVER_PORT & "/status"
    
    ' HTTPリクエストを作成
    Dim http As Object
    Set http = CreateObject("MSXML2.XMLHTTP")
    
    ' リクエストを送信
    http.Open "GET", url, False
    http.send
    
    If http.Status = 200 Then
        ' ステータス情報を表示
        MsgBox "サーバーステータス:" & vbCrLf & vbCrLf & http.responseText, _
               vbInformation, "サーバーステータス"
    Else
        MsgBox "サーバーに接続できませんでした。", vbCritical, "エラー"
    End If
    
    Set http = Nothing
End Sub

'
' 使用例: ボタンから呼び出す
'
Sub Example_GenerateCaseNumber()
    ' 輸出案件番号を生成
    Dim caseNumber As String
    caseNumber = GenerateCaseNumberFromServer("EX", "山田")
    
    If caseNumber <> "" Then
        MsgBox "生成された案件番号: " & caseNumber, vbInformation, "成功"
        
        ' 案件番号をセルに入力（例: アクティブセル）
        ActiveCell.Value = caseNumber
    Else
        MsgBox "案件番号の生成に失敗しました。", vbCritical, "エラー"
    End If
End Sub

'
' 使用例: ヘルスチェック
'
Sub Example_CheckHealth()
    If CheckServerHealth() Then
        MsgBox "サーバーは正常に動作しています。", vbInformation, "ヘルスチェック"
    Else
        MsgBox "サーバーに接続できません。" & vbCrLf & _
               "サーバーが起動しているか確認してください。", _
               vbExclamation, "ヘルスチェック"
    End If
End Sub


