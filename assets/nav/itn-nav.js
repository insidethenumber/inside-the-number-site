/* ══════════════════════════════════════════════════════════════════════════
   ITN global navigation behaviour — Phase 1 (Sep 18 2026)

   One file for every page. It replaces twelve near-identical inline
   hamburger snippets. Nothing here creates navigation: every link is already
   in the HTML, crawlable, and works with JavaScript off. This file only adds
   the disclosure behaviour on top.

   Accessibility contract:
     - each desktop group is a <button aria-expanded> controlling a menu
     - Escape closes and returns focus to the button
     - Tab out of a group closes it
     - clicking anywhere outside closes it
     - the mobile panel traps nothing and closes on Escape or on any link
   ══════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var openGroup = null;
  function closeGroup(restoreFocus) {
    if (!openGroup) return;
    var btn = openGroup.querySelector('.itn-top');
    var menu = openGroup.querySelector('.itn-menu');
    if (btn) btn.setAttribute('aria-expanded', 'false');
    if (menu) menu.hidden = true;
    if (restoreFocus && btn) btn.focus();
    openGroup = null;
  }

  function wireGroups() {
    var groups = document.querySelectorAll('.itn-links .itn-group');
    Array.prototype.forEach.call(groups, function (group) {
      var btn = group.querySelector('.itn-top');
      var menu = group.querySelector('.itn-menu');
      if (!btn || !menu) return;

      menu.hidden = true;
      btn.setAttribute('aria-expanded', 'false');

      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var wasOpen = openGroup === group;
        closeGroup(false);
        if (wasOpen) return;
        btn.setAttribute('aria-expanded', 'true');
        menu.hidden = false;
        openGroup = group;
      });

      // Pointer users expect a hover menu; keyboard users must not have one
      // opened under them, so hover only ever opens, never steals focus.
      group.addEventListener('mouseenter', function () {
        if (window.matchMedia('(max-width:900px)').matches) return;
        if (openGroup && openGroup !== group) closeGroup(false);
        btn.setAttribute('aria-expanded', 'true');
        menu.hidden = false;
        openGroup = group;
      });
      group.addEventListener('mouseleave', function () {
        if (window.matchMedia('(max-width:900px)').matches) return;
        if (group.contains(document.activeElement)) return;
        /* CSS owns desktop hover visibility. Do not hide the menu here: a
           mouseleave can fire while the pointer is crossing into the menu,
           and CSS :hover/:focus-within handles the actual boundary safely. */
      });

      // Tabbing past the last item in the menu should close it rather than
      // leave an open panel floating behind the next link.
      group.addEventListener('focusout', function () {
        window.setTimeout(function () {
          if (openGroup === group && !group.contains(document.activeElement)) {
            closeGroup(false);
          }
        }, 0);
      });
    });

    document.addEventListener('click', function (e) {
      if (openGroup && !openGroup.contains(e.target)) closeGroup(false);
    });
  }

  function wireMobile() {
    var btn = document.getElementById('itnMenuButton');
    var panel = document.getElementById('itnMobileMenu');
    if (!btn || !panel) return;

    function close() {
      btn.classList.remove('open');
      panel.classList.remove('open');
      document.body.classList.remove('menu-open');
      btn.setAttribute('aria-expanded', 'false');
    }
    function open() {
      btn.classList.add('open');
      panel.classList.add('open');
      document.body.classList.add('menu-open');
      btn.setAttribute('aria-expanded', 'true');
      var first = panel.querySelector('a');
      if (first) first.focus();
    }

    btn.addEventListener('click', function () {
      if (panel.classList.contains('open')) { close(); btn.focus(); }
      else { open(); }
    });
    Array.prototype.forEach.call(panel.querySelectorAll('a'), function (a) {
      a.addEventListener('click', close);
    });

    // A resize past the breakpoint would otherwise leave the body locked
    // with an invisible panel still "open".
    window.addEventListener('resize', function () {
      if (!window.matchMedia('(max-width:900px)').matches &&
          panel.classList.contains('open')) close();
    });

    window.__itnCloseMobile = close;
  }

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape' && e.key !== 'Esc') return;
    if (openGroup) { closeGroup(true); return; }
    if (typeof window.__itnCloseMobile === 'function') window.__itnCloseMobile();
  });

  function boot() { wireGroups(); wireMobile(); }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
