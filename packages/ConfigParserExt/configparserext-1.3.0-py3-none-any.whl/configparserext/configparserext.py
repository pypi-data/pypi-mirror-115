
'''Expansion of python configparser module

Insert description here
'''

import configparser
import logging
from pathlib import Path
# import sys
from collections import OrderedDict as _default_dict
import beetools

_path = Path(__file__)
_name = _path.stem
_VERSION = '1.2.0'

class ConfigParserExt( configparser.ConfigParser ):
    '''Insert description here
    '''
    def __init__( self, p_parent_logger_name, defaults = None, dict_type = _default_dict, allow_no_value = False, delimiters = ('=', ':'),
                  comment_prefixes = ('#', ';'), inline_comment_prefixes = None, strict = True, empty_lines_in_values = True,
                  default_section = configparser.DEFAULTSECT, interpolation = configparser._UNSET, converters = configparser._UNSET ):
        '''Insert description here
        '''
        self.success = False
        self.logger_name = '{}.{}'.format( p_parent_logger_name, _name )
        self.logger = logging.getLogger( self.logger_name )
        self.logger.info( 'Start' )
        self.version = _VERSION
        super().__init__( defaults = defaults, dict_type = dict_type, allow_no_value = allow_no_value, delimiters = delimiters,
                          comment_prefixes = comment_prefixes, inline_comment_prefixes = inline_comment_prefixes, strict = strict,
                          empty_lines_in_values = empty_lines_in_values, default_section = default_section, interpolation = interpolation,
                          converters = converters )
    # end __init__

    def get( self, p_section, p_option, p_prefix = False, p_split = False, raw = False, vars = None, fallback = configparser._UNSET):
        '''Insert description here
        '''
        def split_value( p_value ):
            value_parsed = p_value.split( ';' )
            return value_parsed
        # end split_value

        if p_prefix:
            value_series = []
            option_series = self.options( p_section, p_option )
            for option in option_series:
                value_parsed = super().get( p_section, option, raw = raw, vars = vars, fallback = fallback )
                if p_split:
                    value_parsed = split_value( value_parsed )
                value_series.append([ option, value_parsed ])
        else:
            value_series = super().get( p_section, p_option, raw = raw, vars = vars, fallback = fallback )
            if p_split:
                value_series = split_value( value_series )
        return value_series
    # end get

    def options( self, p_section, p_option_prefix = False ):
        '''Insert description here
        '''
        all_options = series = super().options( p_section )
        if p_option_prefix:
            series = []
            for option in sorted( all_options ):
                x = len( p_option_prefix )
                if option[ : x ].lower() == p_option_prefix.lower():
                    series.append( option )
        return series
    # end get

    def sections( self, p_section_prefix = False ):
        '''Insert description here
        '''
        all_sections = series = super().sections()
        if p_section_prefix:
            series = []
            for section in all_sections:
                x = len( p_section_prefix )
                if section[ : x ] == p_section_prefix:
                    series.append( section )
        return series
    # end sections
# end ConfigParserExt

def do_examples(p_app_path=None, p_cls=True):
    '''Insert description here
    '''
    def basic_test(p_app_path=None, p_cls=True):
        '''Basic and mandatory scenario tests for certification of the class
        '''
        success = True
        t_series_prefix = 'Series'
        t_sections_01 = [ 'General', 'Series01', 'Series02', 'Series03' ]
        t_sections_02 = [ 'Series01', 'Series02', 'Series03' ]
        t_options_01 = [ 'cmd1', 'cmd2', 'str1', 'str2' ]
        t_options_02 = [ 'cmd1', 'cmd2' ]
        t_value_01 = 'sudo;rm;-f;/etc/nginx/sites-available/\$URL.\$EXT.conf'
        t_value_02 = 'sudo;rm;-R;-f;$www_dir/\$URL.\$EXT'
        t_value_03 = [[ 'cmd1', 'sudo;rm;-f;/etc/nginx/sites-available/\$URL.\$EXT.conf'],
                                [ 'cmd2', 'sudo;rm;-R;-f;$www_dir/\$URL.\$EXT' ]]
        # t_value_split_01 = [[ 'sudo' ], [ 'rm' ], [ '-f' ]            , [ '/etc/nginx/sites-available/\\$URL.\\$EXT.conf' ]]
        # t_value_split_02 = [[ 'sudo' ], [ 'rm' ], [ '-R', '-f' ], [ '$www_dir/\\$URL.\\$EXT' ]]
        # t_value_split_03 = [['cmd1', [['sudo'], ['rm'], ['-f'], ['/etc/nginx/sites-available/\\$URL.\\$EXT.conf']]],
        #                                    ['cmd2', [['sudo'], ['rm'], ['-R', '-f'], ['$www_dir/\\$URL.\\$EXT']]]]
        # t_value_split_01 = [ 'sudo', 'rm', '-f'            , '/etc/nginx/sites-available/\\$URL.\\$EXT.conf' ]
        # t_value_split_02 = [ 'sudo', 'rm', '-R', '-f', '$www_dir/\\$URL.\\$EXT' ]
        t_value_split_03 = [[ 'cmd1', [ 'sudo', 'rm', '-f', '/etc/nginx/sites-available/\\$URL.\\$EXT.conf']],
                            [ 'cmd2', [ 'sudo', 'rm', '-R', '-f', '$www_dir/\\$URL.\\$EXT']]]
        t_cfg_ext = ConfigParserExt( _name )
        t_cfg_ext['General'] = {
            'SeriesPrefix': 'Series',
            'OptionPrefix': 'Cmd'
        }
        t_cfg_ext['Series01'] = {
            'Cmd1': 'ls',
            'Cmd2': 'll',
            'Val1': 1,
            'Val2': 2
        }
        t_cfg_ext['Series02'] = {
            'Cmd1': 'sudo;rm;-f;/etc/nginx/sites-available/\$URL.\$EXT.conf',
            'Cmd2': 'sudo;rm;-R;-f;$www_dir/\$URL.\$EXT',
            'Str1': 'c',
            'Str2': 'd'
        }
        t_cfg_ext['Series03'] = {
            'Cmd1': 5,
            'Cmd2': 6,
            'Str1': 'e',
            'Str2': 'f'
        }
        sections_series = t_cfg_ext.sections()
        if sections_series != t_sections_01:
            success = False and success
            beetools.result_rep( success, 't_sections_01' )
        series_prefix = t_cfg_ext.get( 'General', 'SeriesPrefix' )
        if series_prefix != t_series_prefix:
            success = False and success
            beetools.result_rep( success, 't_series_prefix' )
        sections_series = t_cfg_ext.sections( series_prefix )
        if sections_series != t_sections_02:
            success = False and success
            beetools.result_rep( success, 't_sections_02' )
        option_prefix = t_cfg_ext.get( 'General', 'OptionPrefix' )
        option_series = t_cfg_ext.options( 'Series02' )
        if option_series != t_options_01:
            success = False and success
            beetools.result_rep( success, 't_options_01' )
        option_series = t_cfg_ext.options( 'Series02', qoption_prefix )
        if option_series != t_options_02:
            success = False and success
            beetools.result_rep( success, 't_options_02' )
        value = t_cfg_ext.get( 'Series02', 'Cmd1' )
        if value != t_value_01:
            success = False and success
            beetools.result_rep( success, 't_value_01' )
        value = t_cfg_ext.get( 'Series02', 'Cmd2' )
        if value != t_value_02:
            success = False and success
            beetools.result_rep( success, 't_value_02' )
        value_series = t_cfg_ext.get( 'Series02', 'Cmd', p_prefix = True )
        if value_series != t_value_03:
            success = False and success
            beetools.result_rep( success, 't_value_03' )
        value_series = t_cfg_ext.get( 'Series02', 'Cmd', p_prefix = True, p_split = True )
        if value_series != t_value_split_03:
            success = False and success
            beetools.result_rep( success, 't_value_split_03' )
        beetools.result_rep( success, 'Completed' )
        return success
    # end basic_test

    b_tls = beetools.Archiver(__name__, _VERSION, __doc__.split('\n')[0], p_app_path)
    logger = logging.getLogger( _name )
    logger.setLevel( beetools.DEF_LOG_LEV )
    file_handle = logging.FileHandler( beetools.LOG_FILE_NAME, mode = 'w' )
    file_handle.setLevel( beetools.DEF_LOG_LEV_FILE )
    console_handle = logging.StreamHandler()
    console_handle.setLevel( beetools.DEF_LOG_LEV_CON )
    file_format = logging.Formatter( beetools.LOG_FILE_FORMAT, datefmt = beetools.LOG_DATE_FORMAT )
    console_format = logging.Formatter( beetools.LOG_CONSOLE_FORMAT )
    file_handle.setFormatter( file_format )
    console_handle.setFormatter( console_format )
    logger.addHandler( file_handle )
    logger.addHandler( console_handle )

    b_tls.print_header( p_cls = p_cls )
    print( beetools.msg_milestone( '==[ Start Testing ConfigParserExt ]========================' ))
    success = basic_test()
    beetools.result_rep( success, 'Completed' )
    print( beetools.msg_milestone( '--[ End Testing ConfigParserExt ]---------------------------' ))
    b_tls.print_footer()
    if success:
        return b_tls.archive_path
    return False
# end do_tests

if __name__ == '__main__':
    do_examples(p_app_path=_path)
# end __main__
