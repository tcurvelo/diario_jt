#!/usr/bin/env python
# -*- encoding: utf-8
import os

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait

# Configura o profile do firefox e define caminho para download
fp = webdriver.FirefoxProfile('./firefox_profile')
download_dir = os.getcwd()
fp.set_preference("browser.download.dir", download_dir)
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("pdfjs.migrationVersion", 1);


# Inicia o display e o browser
display = Display(visible=0, size=(800, 600))
display.start()
browser = webdriver.Firefox(fp)


# Abre a pagina inicial do diario
browser.get('http://aplicacao2.jt.jus.br/dejt/')
assert browser.title == u"Diário Eletrônico da Justiça do Trabalho"


# Clica no link 'pesquisar diario'
browser.find_element_by_link_text(u"Pesquisar Diário").click()
assert browser.title == u"Pesquisar Diários"


# Seleciona o regional no combo box
Select(
    browser.find_element_by_id("corpo:formulario:tribunal")
).select_by_visible_text(u"TRT 13ª Região")


# Clica no botao pesquisar
browser.find_element_by_id("corpo:formulario:botaoAcaoPesquisar").click()
elem = browser.find_elements_by_xpath(
    '//*[@id="diarioCon"]/fieldset/table/tbody/tr[2]/td[2]/span'
)[0]
assert u"Caderno do TRT da 13\xaa REGI\xc3O" in elem.text


# Clica no botao de baixar o diario
browser.find_element_by_css_selector("button.bt.af_commandButton").click()

# Espera conclusao do download
WebDriverWait(browser, 20).until(
    lambda x: len(
        [True for arquivo in os.listdir(download_dir) if '.part' in arquivo]
    ) == 0
)


# Encerra o browser e o display
browser.quit()
display.stop()
