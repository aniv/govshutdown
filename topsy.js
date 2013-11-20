all_data = [];

strip = function(html) {
   var tmp = document.createElement("DIV");
   tmp.innerHTML = html;
   return tmp.textContent || tmp.innerText || "";
}

send_data = function() { 
	$.post("http://aniv.info/save.php", JSON.stringify(all_data.pop()), function(status) { 
		if (all_data.length == 0) {
			return;
		}
		else {
			setTimeout(function() { send_data(); }, 100);
		}
	})
}

$(".trending-result").each(function(i){
   tw = $(this).find('.tweet-result-copy');
   twn = $(this).find('.tweet-result-name');
   twm = $(this).find('.precedence-link');
   data = new Object();
   data.index = i;
   data.date = $(this).attr('data-timestamp');
   data.username = $(twn.html()).attr('data-username');
   data.retweets_and_replies = twm.html();
   data.tweet = strip(tw.html());
   data.tweet = data.tweet.replace(/\"/g, " ");
   data.tweet = data.tweet.replace(/\'/g, " ");
   all_data.push(data);
});

console.log(all_data.length)

send_data();