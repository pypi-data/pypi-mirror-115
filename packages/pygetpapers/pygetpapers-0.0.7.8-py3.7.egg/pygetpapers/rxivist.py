import time
import os
import json
import logging
import requests
from pygetpapers.download_tools import DownloadTools


class Rxivist:
    """Rxivist class which handles the rxivist wrapper"""

    def __init__(self):
        """initiate Rxivist class"""
        self.download_tools = DownloadTools("rxivist")
        self.get_url = self.download_tools.posturl

    def rxivist(self,
                query,
                size,
                update=None,
                makecsv=False,
                makexml=False,
                makehtml=False,):
        """Request for the papers and returns the dict

        :param query: the query given to the repo
        :type query: string
        :param size: number of results to get
        :type size: int
        :param update: dict containing old papers, defaults to None
        :type update: dict, optional
        :param makecsv: wheather to make the csv file, defaults to False
        :type makecsv: bool, optional
        :param makexml: wheather to make the xml file, defaults to False
        :type makexml: bool, optional
        :param makehtml: wheather to make the html file, defaults to False
        :type makehtml: bool, optional
        """
        if update:
            cursor_mark = update["cursor_mark"]
        else:
            cursor_mark = 0
        total_number_of_results = size
        total_papers_list = []
        logging.info("Making Request to rxivist")
        while len(total_papers_list) < size:
            total_number_of_results, total_papers_list, papers_list = self.make_request_add_papers(
                query,
                cursor_mark,
                total_number_of_results,
                total_papers_list,
            )
            cursor_mark += 1
            if len(papers_list) == 0:
                logging.warning("Could not find more papers")
                break

        total_result_list = total_papers_list[:size]
        json_return_dict = self.download_tools.make_dict_from_returned_list(
            total_result_list, key_in_dict="doi"
        )
        for paper in json_return_dict:
            self.download_tools.add_keys_for_conditions(
                paper, json_return_dict)
        result_dict = self.download_tools.make_dict_to_return(
            cursor_mark, json_return_dict, total_number_of_results, update=update
        )
        new_dict_to_return = result_dict["new_results"]
        return_dict = new_dict_to_return["total_json_output"]
        self.download_tools.handle_creation_of_csv_html_xml(
            makecsv=makecsv,
            makehtml=makehtml,
            makexml=makexml,
            return_dict=return_dict,
            name="rxivist-result",
        )
        return result_dict

    def send_post_request(self, query, cursor_mark=0, page_size=20):
        url_to_request = self.get_url.format(
            query=query, cursor=cursor_mark, page_size=page_size)
        start = time.time()
        request_handler = requests.get(url_to_request)
        stop = time.time()
        logging.debug("*/Got the Query Result */")
        logging.debug("Time elapsed: %s", (stop - start))
        return request_handler

    def make_request_add_papers(
        self, query, cursor_mark, total_number_of_results, total_papers_list
    ):
        """posts the request and adds the results to the lists

        :param query: the query given to the repo
        :type query: string
        :param cursor_mark: cursor mark
        :type cursor_mark: string
        :param total_number_of_results: total number of results
        :type total_number_of_results: int
        :param total_papers_list: list containing all the papers
        :type total_papers_list: list
        :return: total_number_of_results, total_papers_list, papers_list
        :rtype: tuple
        """
        request_handler = self.send_post_request(query, cursor_mark)
        request_dict = json.loads(request_handler.text)
        papers_list = request_dict["results"]
        if "total_results" in request_dict["query"]:
            total_number_of_results = request_dict["query"]["total_results"]
        total_papers_list += papers_list
        return total_number_of_results, total_papers_list, papers_list

    def rxivist_update(
        self,
        query,
        size,
        update=None,
        makecsv=False,
        makexml=False,
        makehtml=False,
    ):
        """Handles rxivist update

        :param interval: interval to get papers from
        :type interval: string
        :param size: number of results to get
        :type size: int
        :param update: dict containing old papers, defaults to None
        :type update: dict, optional
        :param makecsv: wheather to make the csv file, defaults to False
        :type makecsv: bool, optional
        :param makexml: wheather to make the xml file, defaults to False
        :type makexml: bool, optional
        :param makehtml: wheather to make the html file, defaults to False
        :type makehtml: bool, optional
        """
        os.chdir(os.path.dirname(update))
        update = self.download_tools.readjsondata(update)
        logging.info("Reading old json metadata file")
        self.download_and_save_results(
            query,
            size,
            update=update,
            makecsv=makecsv,
            makexml=makexml,
            makehtml=makehtml,
        )

    def download_and_save_results(
        self,
        query,
        size,
        update=False,
        makecsv=False,
        makexml=False,
        makehtml=False,
    ):
        """Downloads and saves the results

        :param query: the query given to the repo
        :type query: string
        :param size: number of results to get
        :type size: int
        :param makecsv: wheather to make the csv file, defaults to False
        :type makecsv: bool, optional
        :param makexml: wheather to make the xml file, defaults to False
        :type makexml: bool, optional
        :param makehtml: wheather to make the html file, defaults to False
        :type makehtml: bool, optional
        """
        result_dict = self.rxivist(
            query,
            size,
            update=update,
            makecsv=makecsv,
            makexml=makexml,
            makehtml=makehtml,
        )
        self.download_tools.make_json_files_for_paper(
            result_dict["new_results"], updated_dict=result_dict["updated_dict"], key_in_dict="doi", name_of_file="rxivist-result"
        )

    def noexecute(self, query):
        """no execute for rxivist

        :param query: the query given to the repo
        :type query: string
        """
        result_dict = self.rxivist(query, size=10)
        totalhits = result_dict["new_results"]["total_hits"]
        logging.info("Total number of hits for the query are %s", totalhits)
