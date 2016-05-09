from splinter import Browser
from time import sleep

with Browser() as browser:
    url = "http://www.theatlantic.com/"
    browser.visit(url)
    sleep(5.0)  # wait for whole thing to load
    form = browser.find_by_css('#footer-newsletter-signup form').first
    checkboxes = form.find_by_css('input[type="checkbox"]')
    for checkbox in checkboxes:
        # checkbox.click()
        checkbox.check()
        sleep(0.1)
    email_input = form.find_by_css('input[type="email"]').first
    email_input.fill('op.eter.s@theatlantic.com')
    
    submit_button = form.find_by_css('input[type="submit"]').first
    submit_button.click()

    # Verify
    message_box = form.find_by_css('.message.success').first
    if message_box.visible:
        print("Success!")
    else:
        print("Failure")


    print("try: ")
    import ipdb
    ipdb.set_trace()
    print()
