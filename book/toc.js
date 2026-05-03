// Populate the sidebar
//
// This is a script, and not included directly in the page, to control the total size of the book.
// The TOC contains an entry for each page, so if each page includes a copy of the TOC,
// the total size of the page becomes O(n**2).
class MDBookSidebarScrollbox extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML = '<ol class="chapter"><li class="chapter-item expanded "><a href="cover.html"><strong aria-hidden="true">1.</strong> 封面</a></li><li class="chapter-item expanded "><a href="toc.html"><strong aria-hidden="true">2.</strong> 目录</a></li><li class="chapter-item expanded "><a href="preamble.html"><strong aria-hidden="true">3.</strong> 前言</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded affix "><li class="part-title">第一部分 基础与框架</li><li class="chapter-item expanded "><a href="part1.html"><strong aria-hidden="true">4.</strong> 第一部分导读</a></li><li class="chapter-item expanded "><a href="ch01-overview.html"><strong aria-hidden="true">5.</strong> 第1章 Agent Memory 全景地图</a></li><li class="chapter-item expanded "><a href="ch02-ontology.html"><strong aria-hidden="true">6.</strong> 第2章 本体论框架</a></li><li class="chapter-item expanded "><a href="ch03-cognitive.html"><strong aria-hidden="true">7.</strong> 第3章 认知科学映射</a></li><li class="chapter-item expanded affix "><li class="part-title">第二部分 短期记忆层</li><li class="chapter-item expanded "><a href="part2.html"><strong aria-hidden="true">8.</strong> 第二部分导读</a></li><li class="chapter-item expanded "><a href="ch04-context-as-memory.html"><strong aria-hidden="true">9.</strong> 第4章 上下文窗口作为记忆</a></li><li class="chapter-item expanded "><a href="ch05-context-compression.html"><strong aria-hidden="true">10.</strong> 第5章 上下文压缩与注意力分配</a></li><li class="chapter-item expanded "><a href="ch06-working-memory-manager.html"><strong aria-hidden="true">11.</strong> 第6章 工作记忆管理器</a></li><li class="chapter-item expanded affix "><li class="part-title">第三部分 长期记忆层</li><li class="chapter-item expanded "><a href="part3.html"><strong aria-hidden="true">12.</strong> 第三部分导读</a></li><li class="chapter-item expanded "><a href="ch07-episodic-semantic.html"><strong aria-hidden="true">13.</strong> 第7章 情景记忆与语义记忆</a></li><li class="chapter-item expanded "><a href="ch08-storage-architecture.html"><strong aria-hidden="true">14.</strong> 第8章 记忆存储架构选型</a></li><li class="chapter-item expanded "><a href="ch09-retrieval-reasoning.html"><strong aria-hidden="true">15.</strong> 第9章 检索增强与多跳推理</a></li><li class="chapter-item expanded "><a href="ch10-memory-dialogue.html"><strong aria-hidden="true">16.</strong> 第10章 构建记忆增强对话系统</a></li><li class="chapter-item expanded affix "><li class="part-title">第四部分 程序性记忆层</li><li class="chapter-item expanded "><a href="part4.html"><strong aria-hidden="true">17.</strong> 第四部分导读</a></li><li class="chapter-item expanded "><a href="ch11-procedural-memory.html"><strong aria-hidden="true">18.</strong> 第11章 经验、技能、工具使用记忆</a></li><li class="chapter-item expanded "><a href="ch12-reflection-system.html"><strong aria-hidden="true">19.</strong> 第12章 自我反思与经验积累系统</a></li><li class="chapter-item expanded "><a href="ch13-cross-session.html"><strong aria-hidden="true">20.</strong> 第13章 跨会话学习与个性化</a></li><li class="chapter-item expanded affix "><li class="part-title">第五部分 治理与前沿</li><li class="chapter-item expanded "><a href="part5.html"><strong aria-hidden="true">21.</strong> 第五部分导读</a></li><li class="chapter-item expanded "><a href="ch14-governance.html"><strong aria-hidden="true">22.</strong> 第14章 记忆治理</a></li><li class="chapter-item expanded "><a href="ch15-roadmap-future.html"><strong aria-hidden="true">23.</strong> 第15章 工程决策地图与未来展望</a></li><li class="chapter-item expanded "><a href="ch16-comprehensive-case.html"><strong aria-hidden="true">24.</strong> 第16章 综合案例：记忆增强的个人研究助手</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded "><a href="appendix.html"><strong aria-hidden="true">25.</strong> 附录</a></li></ol>';
        // Set the current, active page, and reveal it if it's hidden
        let current_page = document.location.href.toString().split("#")[0].split("?")[0];
        if (current_page.endsWith("/")) {
            current_page += "index.html";
        }
        var links = Array.prototype.slice.call(this.querySelectorAll("a"));
        var l = links.length;
        for (var i = 0; i < l; ++i) {
            var link = links[i];
            var href = link.getAttribute("href");
            if (href && !href.startsWith("#") && !/^(?:[a-z+]+:)?\/\//.test(href)) {
                link.href = path_to_root + href;
            }
            // The "index" page is supposed to alias the first chapter in the book.
            if (link.href === current_page || (i === 0 && path_to_root === "" && current_page.endsWith("/index.html"))) {
                link.classList.add("active");
                var parent = link.parentElement;
                if (parent && parent.classList.contains("chapter-item")) {
                    parent.classList.add("expanded");
                }
                while (parent) {
                    if (parent.tagName === "LI" && parent.previousElementSibling) {
                        if (parent.previousElementSibling.classList.contains("chapter-item")) {
                            parent.previousElementSibling.classList.add("expanded");
                        }
                    }
                    parent = parent.parentElement;
                }
            }
        }
        // Track and set sidebar scroll position
        this.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                sessionStorage.setItem('sidebar-scroll', this.scrollTop);
            }
        }, { passive: true });
        var sidebarScrollTop = sessionStorage.getItem('sidebar-scroll');
        sessionStorage.removeItem('sidebar-scroll');
        if (sidebarScrollTop) {
            // preserve sidebar scroll position when navigating via links within sidebar
            this.scrollTop = sidebarScrollTop;
        } else {
            // scroll sidebar to current active section when navigating via "next/previous chapter" buttons
            var activeSection = document.querySelector('#sidebar .active');
            if (activeSection) {
                activeSection.scrollIntoView({ block: 'center' });
            }
        }
        // Toggle buttons
        var sidebarAnchorToggles = document.querySelectorAll('#sidebar a.toggle');
        function toggleSection(ev) {
            ev.currentTarget.parentElement.classList.toggle('expanded');
        }
        Array.from(sidebarAnchorToggles).forEach(function (el) {
            el.addEventListener('click', toggleSection);
        });
    }
}
window.customElements.define("mdbook-sidebar-scrollbox", MDBookSidebarScrollbox);
