sap.registerPlugin(SplitText);

document.addEventListener("DOMContentLoaded", () => {
	gsap.set(".split", { opacity: 1 });

	let split;
	SplitText.create(".split", {
		type: "chars",
		autoSplit: true,
		charsClass: "char",
		autoSplit: true,
		mask: "chars",
		onSplit: (self) => {
			split = gsap.from(self.chars, {
				yPercent: "random([-100, 100])",
				rotation: "random(-30, 30)",
				ease: "back.out",
				autoAlpha: 0,
				stagger: 0.05,
				repeat: -1,
				yoyo: true,
				duration: 0.6
			});
			return split;
		}
	});

	document.querySelector("#speed").addEventListener("input", function () {
		var step = this.value;
		split.timeScale(step).play(0);
	});
});
