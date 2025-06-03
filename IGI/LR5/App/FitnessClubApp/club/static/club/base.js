function refreshTimezone() {
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  document.cookie = "django_timezone=" + timezone;
}
refreshTimezone();
setInterval(refreshTimezone, 5000)


const checks = document.querySelectorAll('.staree')
checks[Date.now() % checks.length].addEventListener('click', () => location.href = (checks[0].className.split(' ')[0]))