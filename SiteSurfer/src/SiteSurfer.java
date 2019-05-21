import java.util.LinkedList;
import java.util.Queue;
import org.jsoup.Jsoup;
import org.jsoup.nodes.*;
import org.jsoup.select.Elements;

import java.util.List;
import java.io.IOException;

public class SiteSurfer {
	static List<String> ExtractLinks(String Url) {
		Document doc = null;
		List<String> str_links = new LinkedList<String>();
		try {
			doc = Jsoup.connect(Url).get();
		} catch (IOException e) {
			e.printStackTrace();
			return str_links;
		}
		Elements links = doc.select("a[href]");
		for (Element link : links){		
		  str_links.add(link.attr("abs:href"));
		}
		return str_links;
	}
	
	public static void main(String[] args) {
		Queue<String> URL_Q = new LinkedList<>(); 
		String start = "http://moz.com/top500";
		URL_Q.add(start);
		String curr;
		while (URL_Q.size() > 0) {
			curr = URL_Q.remove();
			System.out.println(curr);
			for (String link: ExtractLinks(curr)) {
				//System.out.println(link);
				URL_Q.add(link);
			}
		}
	}
}
