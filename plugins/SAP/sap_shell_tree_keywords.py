#-------------------------------------------------------------------------------
# Name:        SAP_Shell_Tree_keywords
# Purpose:     Handling SAP-Shell-Tree elements
#
# Author:      anas.ahmed
#
# Created:     11-12-2019
# Copyright:   (c) anas.ahmed 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sap_constants
from constants import *
import logger
from saputil_operations import SapUtilKeywords
from sap_launch_keywords import Launch_Keywords
import logging
log = logging.getLogger("sap_shell_tree_keywords.py")

class Shell_Tree_Keywords():
    def __init__(self):
        self.uk = SapUtilKeywords()
        self.lk = Launch_Keywords()

    #TREE
    #---------------------------------------------------------------------------shell tree suppliment functions

    def tree_Type(self, elem):
        tree_type = None
        try:
            tree_type = elem.GetTreeType()
            if ( tree_type == 0 ):
                log.debug( 'Simple Tree' )
            elif ( tree_type == 1 ):
                log.debug( 'List Tree' )
            elif ( tree_type == 2 ):
                log.debug( 'Column Tree' )
        except Exception as e:
            log.error( e )
        return tree_type

    def treeTraverse(self, elem , input_val, column_data):
        treeType = self.tree_Type(elem)
        flag = False
        #-----------------------------------------------------------------------
        #-----------------------------------------------------------------------
        if ( not( column_data ) ):
            #list tree and simple
            cflag = True
            for i in range(0, len(input_val)):
                if ( i == 0 ):
                    node = elem.TopNode
                    try:
                        if ( input_val[i].isdigit() ):
                            count = int( input_val[i] )
                            c = self.getFirstLevelNodeCount(elem)
                            if ( count > c ):
                                cflag = False
                                break
                            try:
                                while ( count - 1 ):
                                    node = elem.GetNextNodeKey(node)
                                    count = count - 1
                            except:
                                pass
                        else:
                            try:
                                txt = self.getTextofNode(elem, node)
                                while txt.lower() != input_val[i].lower():
                                    node = elem.GetNextNodeKey(node)
                                    txt = self.getTextofNode(elem, node)
                            except:
                                pass
                    except:
                        pass
                else:
                    self.expandTree(elem, node)
                    child_nodes = elem.GetSubNodesCol(node)
                    try:
                        if ( input_val[i].isdigit() ):
                            count = int( input_val[i] )
                            if ( count > len(child_nodes) ):
                                cflag = False
                                break
                            try:
                                node = child_nodes[0]
                                while (count - 1):
                                    node = elem.GetNextNodeKey(node)
                                    count = count - 1
                            except:
                                pass
                        else:
                            try:
                                node = child_nodes[0]
                                txt = self.getTextofNode(elem, node)
                                while txt.lower() != input_val[i].lower():
                                    node = elem.GetNextNodeKey(node)
                                    txt = self.getTextofNode(elem, node)
                            except:
                                pass
                    except:
                        pass
            txt = self.getTextofNode(elem, node)
            if ( not ( input_val[len(input_val) - 1].isdigit() ) ):
                if ( txt.lower() == input_val[len(input_val) - 1].lower() ):
                    flag = True
            elif ( cflag ):
                flag = True
        #-----------------------------------------------------------------------
        #-----------------------------------------------------------------------
        elif ( column_data and treeType == 2 ):
            #column
            if ( column_data ):
                verifyColVal = ( len(column_data) >= 1 ) and ( elem.GetTreeType() == 2 )
                if ( verifyColVal ):
                    columnNames = elem.GetColumnNames()
                    titles = [elem.GetColumnTitleFromName(col) for col in columnNames if col]
                for i in range(0, len(input_val)):
                    # ----------------- Loop iteration initialization - Start -----------------------
                    nText = input_val[i]
                    colCheck = False
                    check = False
                    if ( verifyColVal and len(column_data[i]) == 2 ):  # @add Code for Case When Value is Missing
                        colCheck = True
                        col_count = len(titles)
                        col_no = column_data[i][0].strip()
                        if ( col_no.isdigit() ):
                            col_no = int(col_no)
                            if ( col_no > col_count ):
                                err_msg = "Tree Traverse : Column Number specified exceeds the number of columns present in the tree"
                                log.debug( err_msg )
                                log.error( err_msg )
                                return None
                            col_no = col_no - 1
                        else:
                            try:
                                col_no = titles.index(col_no)
                            except ValueError:
                                err_msg = 'Column not found'
                                logger.print_on_console( err_msg )
                                return None
                        col_val = column_data[i][1]
                    # Top Node - Either Inside a Parent or node without a Parent
                    if ( i == 0 ):
                        node = self.getFirstRootNode(elem)
                    else:
                        child_nodes = elem.GetSubNodesCol(node)
                        try:
                            node = child_nodes[0]
                        except Exception as e:
                            log.error( sap_constants.ERROR_MSG + ' : ' + str(e) )
                            log.debug( 'Tree Traverse : No further Children found' )
                            return None
                    self.expandTree(elem, node)
                    #----------------- Loop iteration initialization - End --------------------------
                # check, node, col_no, col_val, col_count, col_check, nText - initialized
                try:
                    if ( colCheck ):
                        columnText = elem.getItemText(node, elem.GetColumnNames()[col_no])
                        check = (columnText.lower() != col_val.lower())

                    if ( nText.isdigit() ):
                        # Part1 - When node index is provided
                        log.debug('Moving to node Number : ' + str(nText))
                        try:
                            for i in range(int(nText) - 1):
                                node = elem.GetNextNodeKey(node)
                        except Exception as e:
                            err_msg = 'Invalid index'
                            log.error( err_msg )
                            log.error( sap_constants.ERROR_MSG + ' : ' + str(e) )
                            logger.print_on_console( err_msg )
                            return None

                        if ( colCheck ):
                            columnText = elem.getItemText(node, elem.GetColumnNames()[col_no])
                            check = columnText.lower() != col_val.lower()
                    else:
                        # Part2 - When node text is provided
                        txt = self.getTextofNode(elem, node)
                        while txt.lower() != nText.lower() or check:
                            try:
                                node = elem.GetNextNodeKey(node)
                                txt = self.getTextofNode(elem, node)
                            except Exception as e:
                                """
                                    Exception will be raised when looping through current level is going on
                                    and the required node is not found so it is definetely a failed case.
                                """
                                err_msg = 'Node not found'
                                log.error( sap_constants.ERROR_MSG + ' : ' + str(e) )
                                log.debug( 'Node with Text = ' + nText + " not found" )
                                logger.print_on_console( err_msg )
                                return None
                            if ( colCheck ):
                                columnText = elem.getItemText(node, elem.GetColumnNames()[col_no])
                                check = (columnText.lower() != col_val.lower())
                        log.debug( 'Moving to node with text : ' + str(txt) )
                    self.expandTree(elem, node)
                except:  # @update code - as exceptions are already handled inside this try check if it is needed for unexpected exceptions or move exceptions that are handled
                    # inside here itself
                    pass
                 # Final Verification of Leaf Node
                txtCheck = True
                """
                   If Leaf Node is an index and node is found at that index then it is assumed that node is correct
                   and if Lead Node is a text then compare the text of the lead provided and actual text.
                """
                if ( not nText.isdigit() ):
                    txt = self.getTextofNode(elem, node)
                    txtCheck = txt.lower() == input_val[len(input_val) - 1].lower()
                if ( verifyColVal ):
                    if ( txtCheck and not check ):
                        flag = True
                    else:
                        flag = False
        #-----------------------------------------------------------------------
        if ( flag ):
            return node
        else:
            return None

    def getTextofNode(self, elem, node):
        txt = None
        if ( elem.GetTreeType() == 2 ):  # @add - add more conditions based on tree types
           cols = elem.GetColumnNames()
           for col in cols:
               txt = elem.GetItemText(node, col)
               if ( txt ):
                   return txt
        else:
            txt = elem.GetNodeTextByKey(node)
        return txt


    def getSelectedNodes(self, elem):
        nodes = []
        if ( elem.GetTreeType() == 2 ):  # @add - add more conditions based on tree types
            nodes = [elem.SelectedItemNode()]
        else:
            nodes = elem.GetSelectedNodes()
        return nodes

    def singleSelectNode(self, elem, node):
        if ( elem.GetTreeType() == 2 ):  # @add - add more conditions based on tree types
            elem.SelectItem(node, elem.GetColumnNames()[0])
        else:
            elem.SelectNode(node)
        return

    def getFirstLevelNodeCount(self, tree):
        c = 1
        n = self.getFirstRootNode(tree)
        while True:
            try:
                n = tree.GetNextNodeKey(n)
                c = c + 1
            except:
                break
        return c

    def expandTree(self, tree, node):
        if ( self.isFolder(tree, node) ):
            if ( tree.IsFolderExpanded(node) != True ):
                try:
                    tree.ExpandNode(node)
                except:
                    pass

    def isFolder(self, tree, node):
        return True if(tree.IsFolder(node) == True or tree.isFolderExpandable(node) == True or tree.GetNodeChildrenCount(node) > 0) else False

    def recursiveCollapseNode(self, tree, node):
        nodes = tree.GetSubNodesCol(node)
        if ( len(nodes) == 0 ):
            return
        for node in nodes:
            if ( self.isFolder(tree, node) and tree.isFolderExpanded(node) ):
                self.recursiveCollapseNode(tree, node)
                tree.CollapseNode(node)

    def getFirstRootNode(self, tree):
        root = tree.TopNode
        while True:
            try:
               parent = tree.GetParent(root)
               if ( parent ):
                   root = parent
               else:
                   break
            except:
                break
        while True:
            try:
                previous = tree.GetPreviousNodeKey(root)
                root = previous
            except:
                break
        return root

    def colData(self, column_data, len_input):
        newL = []
        if ( column_data ) :
            for i in range( 0, len_input - 1 ):
                newL.append([])
            newL.append(column_data)
        else:
            newL = None
        return newL

    #---------------------------------------------------------------------------shell tree suppliment functions
    #---------------------------------------------------------------------------shell tree keywords
    """Keywords : 1.verifyTreePath 2.selectTreeElement 3.getTreeNodeText 4.getTreeNodeCount 5.singleSelectParentOfSelected
    6.collapseTree 7.getColValueCorrToSelectedNode 8.selectTreeNode 9.getNodeNameByIndex """
    def verifyTreePath(self, sap_id, input_val, *args):
        """
            :param sap_id: Object Id of element
            :param input_val: Path to the Node from Top [A<str>; B<str>; C<str>]
            :param column_data: Array of Array containing Column information specific to node
            [['Column_Name<String>','Column_Value<String>'], [Column_Number<int>, Column_Value<String>]]
        """
        #-------------------to split input variables
        index = []
        column_data = None
        for i in range(0,len(input_val)):
            if ( input_val[i] == '<>' ):
                index.append(i)
        if ( index ):
            input_val = input_val[:index[0]]
            column_data = self.colData(input_val[index[0] + 1:],len(input_val))
        #-------------------to split input variables
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        node = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    node = self.treeTraverse(elem, input_val, column_data)
                    if ( node ):
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = "Verification Failed for the path specified in the Tree"
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in VerifyTreePath' )
        return status, result, value, err_msg

    def selectTreeElement(self, sap_id, input_val, *args):
        '''
            :param sap_id: Object Id of SAP element
            :param input_val: Path From Root node to the desired Node. for example - [A,B,C]
            :param column_data: Array of Array containing Column information specific to node
            [['Column_Name<String>','Column_Value<String>'], [Column_Number<int>, Column_Value<String>]]
            :param isDoubleClick: 0 or 1 Indicating whether to double click or not
            :param item: item in Node (row) to double click
            :param args:
        '''
        #-------------------to split input variables
        isDoubleClick=0
        item=None
        column_data = None
        index=[]
        for i in range(0,len(input_val)):
            if ( input_val[i] == '<>' ):
                index.append(i)
        if ( index ):
            if ( len(index) == 1 ):
                input_val = input_val[:index[0]]
                column_data = self.colData(input_val[index[0] + 1:],len(input_val))
            elif ( len(index) == 2 ):
                isDoubleClick = input_val[index[1]+1:][0]
                input_val = input_val[:index[0]]
                column_data = self.colData(input_val[index[0] + 1:index[1]],len(input_val))
            elif ( len(index) == 3 ):
                item = input_val[index[2]+1:][0]
                isDoubleClick = input_val[index[1]+1:index[2]][0]
                input_val = input_val[:index[0]]
                column_data = self.colData(input_val[index[0] + 1:index[1]],len(input_val))
        #-------------------to split input variables

        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        node = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                elem.UnselectAll()
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    node = self.treeTraverse(elem, input_val, column_data)
                    if ( node ):
                        isDoubleClick = int( isDoubleClick )
                        if ( item ):  # Selection When Item is there
                            check = False
                            if ( item.isdigit() ):  # Item is Column Number or Item Index
                                # @add Code - Add Condition of selecting last item when item_no is 0
                                item = int(item)
                                if ( item > 0 ):
                                    tree_type = elem.GetTreeType()
                                    item_id = None
                                    if ( tree_type == 1 ):  # List Tree
                                        log.debug('Operation on item in list at index : ' + str(item))
                                        item_count = elem.GetListTreeNodeItemCount(node)
                                        item_id = item
                                    elif ( tree_type == 2 ):  # Column Tree
                                        columns = elem.GetColumnNames()
                                        item_count = len(columns)
                                        item_id = columns[item - 1]
                                        log.debug('Operation on item at column index : ' + str(item))
                                    check = (item <= item_count)
                                else:
                                    err_msg = 'Invalid Item'
                                    log.debug( err_msg )
                            else:  # Item is Column Name
                                # To get Item ID when item is not a digit but column name
                                columns = elem.GetColumnNames()
                                column_titles = [elem.GetColumnTitleFromName(col) for col in columns]
                                log.debug( 'Avaliable column titles to set item as : ' + str(column_titles) )
                                try:
                                    item_id = columns[column_titles.index(item)]
                                    check = True
                                    log.debug( 'Operation on item with column name : ' + str(item) )
                                except ValueError:
                                    err_msg = 'Column not found'
                                    log.debug( err_msg )
                            if ( check ):
                                elem.SelectItem(node, item_id)
                                if ( isDoubleClick ):
                                    elem.DoubleClickItem(node, item_id)
                                else:
                                    if elem.GetItemType(node, item_id) == 3: #checkbox type
                                        elem.ChangeCheckbox(node, item_id, True)
                                    elif elem.GetItemType(node, item_id) == 4: #button type
                                        elem.PressButton(node, item_id)
                                    elif elem.GetItemType(node, item_id) == 5: #link type
                                        elem.clickLink(node, item_id)

                            else:
                                err_msg = 'Invalid item'
                                log.debug( err_msg )
                        else:
                            # SomeNodes with GetItemType = 2 does not work for Double Click But With SelectedNode
                            # Selection and Double Click Both Operation so as to Select and DoubleClick in cases where Double Click Works and where selected Work
                            elem.SelectNode(node)
                            if ( isDoubleClick ):
                                elem.DoubleClickNode(node)
                        if ( not err_msg ):
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = sap_constants.INVALID_INPUT
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in SelectTreeElement' )
        return status, result, value, err_msg

    def getTreeNodeText(self, sap_id, input_val, *args):
        '''
            :param sap_id: Object Id of SAP element
            :param input_val: Path From Root node to the desired Node. for example - [A,B,C]
            :param column_data: Array of Array containing Column information specific to node
            [['Column_Name<String>','Column_Value<String>'], [Column_Number<int>, Column_Value<String>]]
            :param item: item in Node (row) to double click
            :param args:
        '''
        #-------------------to split input variables
        item = None
        column_data = None
        index = []
        for i in range( 0,len(input_val) ):
            if ( input_val[i] == '<>' ):
                index.append(i)
        if ( index ):
            if ( len(index) == 1 ):
                input_val = input_val[:index[0]]
                column_data = self.colData(input_val[index[0] + 1:],len(input_val))
            elif ( len(index) == 2 ):
                item = input_val[index[1]+1:][0]
                input_val = input_val[:index[0]]
                column_data = self.colData(input_val[index[0] + 1:index[1]],len(input_val))
        #-------------------to split input variables
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        node = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                elem.UnselectAll()
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    node = self.treeTraverse(elem, input_val, column_data)
                    if ( node ):
                        if ( item ):  # Selection When Item is there
                            check = False
                            if ( item.isdigit() ):  # Item is Column Number or Item Index
                                # @add Code - Add Condition of selecting last item when item_no is 0
                                item = int(item)
                                if ( item > 0 ):
                                    tree_type = elem.GetTreeType()
                                    item_id = None
                                    if ( tree_type == 1 ):  # List Tree
                                        log.debug( 'Operation on item in list at index : ' + str(item) )
                                        item_count = elem.GetListTreeNodeItemCount(node)
                                        item_id = item
                                    elif ( tree_type == 2 ):  # Column Tree
                                        columns = elem.GetColumnNames()
                                        item_count = len(columns)
                                        item_id = columns[item - 1]
                                        log.debug('Operation on item at column index : ' + str(item))
                                    check = (item <= item_count)
                                else:
                                    err_msg = 'Invalid item'
                                    log.debug( err_msg )
                            else:  # Item is Column Name
                                # To get Item ID when item is not a digit but column name
                                columns = elem.GetColumnNames()
                                column_titles = [elem.GetColumnTitleFromName(col) for col in columns]
                                try:
                                    item_id = columns[column_titles.index(item)]
                                    check = True
                                    log.debug('Operation on item with column name : ' + str(item))
                                except ValueError:
                                    err_msg = 'Column not found'
                                    log.debug( err_msg )
                            if ( check ):
                                value = elem.GetItemText(node, item_id)
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            else:
                                err_msg = 'Invalid item'
                                log.debug( err_msg )
                        else:
                            value = self.getTextofNode(elem, node)
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = sap_constants.INVALID_INPUT
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in GetTreeNodeText' )
        return status, result, value, err_msg

    def getTreeNodeCount(self, sap_id, input_val, *args):
        '''
                   :param sap_id: Object Id of SAP element
                   :param input_val: Path From Root node to the desired Node. for example - [A,B,C]
                   :param column_data: Array of Array containing Column information specific to node
                   [['Column_Name<String>','Column_Value<String>'], [Column_Number<int>, Column_Value<String>]]
                   :param item: item in Node (row) to double click
                   :param args:
               '''
        #-------------------to split input variables
        index = []
        column_data = None
        for i in range( 0,len(input_val) ):
            if ( input_val[i] == '<>' ):
                index.append(i)
        if ( index ):
            input_val = input_val[:index[0]]
            column_data = self.colData(input_val[index[0] + 1:],len(input_val))
        #-------------------to split input variables
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        node = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                elem.UnselectAll()
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    if ( not( input_val[0] ) ):
                        value = self.getFirstLevelNodeCount(elem)
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        node = self.treeTraverse(elem, input_val, column_data)
                        if ( node ):
                            if ( self.isFolder(elem, node) ):
                                self.expandTree(elem,node)
                                child_nodes = elem.GetSubNodesCol(node)
                                value = len(child_nodes)
                            else:
                                value = 0
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                        else:
                            err_msg = sap_constants.INVALID_INPUT
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in GetTreeNodeCount' )
        return status, result, value, err_msg

    def singleSelectParentOfSelected(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    nodes = self.getSelectedNodes(elem)
                    if ( nodes is not None ):
                        if ( len(nodes) == 1 ):
                            try:
                                parent = elem.GetParent(nodes[0])
                                self.singleSelectNode(elem, parent)
                                status = sap_constants.TEST_RESULT_PASS
                                result = sap_constants.TEST_RESULT_TRUE
                            except Exception as e:
                                log.error(e)
                                err_msg = 'Parent not found'
                        else:
                            err_msg = 'Multiple selection not allowed'
                    else:
                        err_msg = 'Rows not found'
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in singleSelectParentOfSelected' )
        return status, result, value, err_msg

    def collapseTree(self, sap_id, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 3:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    count = self.getFirstLevelNodeCount(elem)
                    for index in range(count):
                        if ( index == 0 ):
                            n = self.getFirstRootNode(elem)
                        else:
                            n = elem.GetNextNodeKey(n)
                        if ( self.isFolder(elem, n) and elem.isFolderExpanded(n) ):
                            log.debug( "Recursively Collapsing Parent Node at index - "+str(index) )
                            self.recursiveCollapseNode(elem, n)
                            elem.CollapseNode(n)
                    status = sap_constants.TEST_RESULT_PASS
                    result = sap_constants.TEST_RESULT_TRUE
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in CollapseTree' )
        return status, result, value, err_msg

    def getColValueCorrToSelectedNode(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    if ( elem.GetTreeType() == 2 ):
                        node = elem.SelectedItemNode()
                        if ( node ):
                            try:
                                colNumber = int(input_val[0])
                                columns = elem.GetColumnNames()
                                if ( colNumber <= len(columns) ):
                                    colNumber = colNumber - 1
                                    value = elem.GetItemText(node, columns[colNumber])
                                    status = sap_constants.TEST_RESULT_PASS
                                    result = sap_constants.TEST_RESULT_TRUE
                                    log.debug( 'Get Column Text From Selected Column => Value is: ' + str(value) )
                                else:
                                    err_msg = 'Col Index Out of Range'
                            except Exception as e:
                                log.error(e)
                                err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
                        else:
                            err_msg = 'No Item Selected'
                    else:
                        err_msg = 'Not a Column Tree'
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in GetColValueCorrToSelectedNode' )
        return status, result, value, err_msg

    def selectTreeNode(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        node = None
        in_flag = False
        additional_data = None
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                elem.UnselectAll()
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    node = self.treeTraverse(elem, input_val, additional_data)
                    if ( node ):
                        # Some Nodes with GetItemType = 2 does not work for Double Click But With SelectedNode
                        # Selection and Double Click Both Operation so as to Select and DoubleClick in cases where DoubleClickNode works so will SelectedNode
                        try:
                            elem.SelectNode(node)
                            elem.DoubleClickNode(node)
                            in_flag = True
                        except:
                            elem.DoubleClickNode(node)
                            in_flag = True
                        if ( in_flag == True ):
                            status = sap_constants.TEST_RESULT_PASS
                            result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = sap_constants.INVALID_INPUT
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in SelectTreeNode' )
        return status,result,value,err_msg

    def getNodeNameByIndex(self, sap_id, input_val, *args):
        status = sap_constants.TEST_RESULT_FAIL
        result = sap_constants.TEST_RESULT_FALSE
        err_msg = None
        value = OUTPUT_CONSTANT
        node = None
        flag = True
        try:
            # get the co-ordinate or position
            if len(args) >= 2:
                sap_position = args[-1]
            else:
                sap_position = {'top': None, 'left': None, 'width': None, 'height': None}

            self.lk.setWindowToForeground(sap_id)
            id, ses = self.uk.getSapElement(sap_id, sap_position)
            if ( id and ses ):
                elem = ses.FindById(id)
                if ( elem.type == 'GuiShell' and elem.SubType == 'Tree' ):
                    for i in range(0,len(input_val)):
                        count = int(input_val[i])
                        if ( i == 0 ):
                            node = elem.TopNode
                            c = self.getFirstLevelNodeCount(elem)
                            if ( count > c ):
                                flag = False
                                break
                            try:
                                while ( count - 1 ):
                                    node = elem.GetNextNodeKey(node)
                                    count = count - 1
                            except:
                                pass
                        else:
                            self.expandTree(elem,node)
                            child_nodes = elem.GetSubNodesCol(node)
                            if ( count > len(child_nodes) ):
                                flag = False
                                break
                            try:
                                node = child_nodes[0]
                                while (count - 1):
                                    node = elem.GetNextNodeKey(node)
                                    count = count - 1
                            except Exception as e:
                                pass
                    if ( flag ):
                        value = elem.GetNodeTextByKey(node)
                        status = sap_constants.TEST_RESULT_PASS
                        result = sap_constants.TEST_RESULT_TRUE
                    else:
                        err_msg = sap_constants.INVALID_INPUT
                else:
                    err_msg = sap_constants.INVALID_ELELMENT_TYPE
            else:
                err_msg = sap_constants.ELELMENT_NOT_FOUND
            #----------------------------------logging
            if ( err_msg ):
                log.info( err_msg )
                logger.print_on_console( err_msg )
        except Exception as e:
            err_msg = sap_constants.ERROR_MSG + ' : ' + str(e)
            log.error( err_msg )
            logger.print_on_console( 'Error occured in GetNodeNameByIndex' )
        return status, result, value, err_msg