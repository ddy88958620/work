<?php
/*
Uploadify
Copyright (c) 2012 Reactive Apps, Ronnie Garcia
Released under the MIT License <http://www.opensource.org/licenses/mit-license.php> 
*/

// Define a destination
$targetFolder = '/xiaoying/uploads'; // Relative to the root

$verifyToken = md5('unique_salt' . $_POST['timestamp']);

if (!empty($_FILES)) {
	$str = time();
	$tempFile = $_FILES['Filedata']['tmp_name'];
	$fileType = pathinfo($_FILES['Filedata']['name']);
	
	$text =$fileType["extension"];
	$fileName = md5($str) . "." . $text;/////重命名
	$targetPath = $_SERVER['DOCUMENT_ROOT'] . $targetFolder;
	$targetFile = rtrim($targetPath,'/') . '/' . $fileName;
	
	// Validate the file type
	$fileTypes = array('jpg','jpeg','gif','png'); // File extensions
	
	$fileParts = pathinfo($fileName);
	
	$strings = json_encode($fileParts);

	if (in_array($fileParts['extension'],$fileTypes)) {
		move_uploaded_file($tempFile,$targetFile);
		
		echo $strings;
	} else {
		echo 1;
	}
}
?>