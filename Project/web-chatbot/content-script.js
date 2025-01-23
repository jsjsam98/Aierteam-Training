// Listen for messages from the side panel
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
	if (request.action === "getInfo") {
		// Get the entire HTML content and base URL
		// let htmlContent = document.documentElement.outerHTML;
		let url = window.location.href;
		let innerText = document.body.innerText;

		let links = Array.from(document.querySelectorAll("a")).map(
			(a) => a.href
		);

		let titles = Array.from(
			document.querySelectorAll("h1, h2, h3, h4, h5, h6")
		).map((h) => h.textContent.trim());

		sendResponse({
			url: url,
			links: links,
			titles: titles,
			innerText: innerText,
		});
	}
});
