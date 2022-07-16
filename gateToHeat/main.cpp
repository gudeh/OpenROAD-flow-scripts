/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   main.cpp
 * Author: gudeh
 *
 * Created on 14 de maio de 2022, 14:25
 */

#include <cstdlib>
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <map>



using namespace std;

#include <iostream>
#include <unordered_set>
#include <boost/geometry.hpp>
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry/geometries/point.hpp>
#include <boost/geometry/geometries/box.hpp>


using point_type   = boost::geometry::model::d2::point_xy<double>;
using box_type     = boost::geometry::model::box<point_type>;
using rtree_node_type = std::pair<box_type, std::string>;
using rtree_type      = boost::geometry::index::rtree<rtree_node_type, boost::geometry::index::rstar<16> >;

void show_rtree()
{
    
cout <<  "  ____________________                    " << endl;
cout <<  "  |    | b   |        |                   " << endl;
cout <<  "  |    |_____|        |                   " << endl;
cout <<  "  |     _____      ___|__       _____     " << endl;
cout <<  "  |    |  a  |    |   | C |    |  d  |    " << endl;
cout <<  "  |    |_____|    |___|___|    |_____|    " << endl;
cout <<  "  |___________________|______             " << endl;
cout <<  "      |  e  |         |  f  |             " << endl;
cout <<  "      |_____|         |_____|             " << endl;
cout << endl;

  
    auto box_a = box_type{point_type{5,5}, point_type{6,6}}; //inside
    auto box_b = box_type{point_type{3,8}, point_type{5,10}}; //corner top
    auto box_c = box_type{point_type{9,5}, point_type{11,6}}; //cross right
    auto box_d = box_type{point_type{15,2}, point_type{17,3}}; //out
    auto box_e = box_type{point_type{4,-2}, point_type{6,0}}; //out
    auto box_f = box_type{point_type{10,-2}, point_type{12,0}}; //out

    auto box_search = box_type{point_type{0,0}, point_type{10,10}};

    rtree_type rtree;

    rtree.insert(rtree_node_type{box_a, "box_a"});
    rtree.insert(rtree_node_type{box_b, "box_b"});
    rtree.insert(rtree_node_type{box_c, "box_c"});
    rtree.insert(rtree_node_type{box_d, "box_d"});
    rtree.insert(rtree_node_type{box_e, "box_e"});
    rtree.insert(rtree_node_type{box_f, "box_f"});
    
    cout << "intersect_nodes: " << endl;
    std::vector<rtree_node_type> intersect_nodes;
    rtree.query(boost::geometry::index::intersects(box_search), std::back_inserter(intersect_nodes));
    for (auto node : intersect_nodes) {
        cout << node.second << endl;
    }
    cout << endl;

    cout << "covered_by_nodes: " << endl;
    std::vector<rtree_node_type> covered_by_nodes;
    rtree.query(boost::geometry::index::covered_by(box_search), std::back_inserter(covered_by_nodes));
    for (auto node : covered_by_nodes) {
        cout << node.second << endl;
    }
    cout << endl;

    cout << "within_nodes: " << endl;
    std::vector<rtree_node_type> within_nodes;
    rtree.query(boost::geometry::index::within(box_search), std::back_inserter(within_nodes));
    for (auto node : within_nodes) {
        cout << node.second << endl;
    }
    cout << endl;

    cout << "overlaps_nodes: " << endl;
    std::vector<rtree_node_type> overlaps_nodes;
    rtree.query(boost::geometry::index::overlaps(box_search), std::back_inserter(overlaps_nodes));
    for (auto node : overlaps_nodes) {
        cout << node.second << endl;
    }
    cout << endl;

    cout << "disjoint_nodes: " << endl;
    std::vector<rtree_node_type> disjoint_nodes;
    rtree.query(boost::geometry::index::disjoint(box_search), std::back_inserter(disjoint_nodes));
    for (auto node : disjoint_nodes) {
        cout << node.second << endl;
    }
    cout << endl;

    cout << "intersect_with_area: (within + overlaps)" << endl;
    std::vector<rtree_node_type> int_area_nodes;
    rtree.query(boost::geometry::index::within(box_search), std::back_inserter(int_area_nodes));
    rtree.query(boost::geometry::index::overlaps(box_search), std::back_inserter(int_area_nodes));
    for (auto node : int_area_nodes) {
        cout << node.second << endl;
    }
    cout << endl;
    
}

struct gate{
    string name="";
//    float x0=0.0;
//    float y0=0.0;
//    float x1=0.0;
//    float y1=0.0;
    vector<int> gatePos;
    float width=0.0;
    float height=0.0;
    vector<float> heatPlacement, heatPower, heatRouting, heatIrdrop;
};

struct heatBbox{
    string name="";
    float x0=0.0;
    float y0=0.0;
    float x1=0.0;
    float y1=0.0;
    float width=0.0;
    float height=0.0;
    float value=0.0;
};
int main(int argc, char** argv) {

    string root="./myStuff";
    vector<string> all_projects;
    for( auto& p : filesystem::directory_iterator( root ) )
    {
        if (p.is_directory() && p.path().string().find("myDataSet") == string::npos)
            all_projects.push_back(p.path().string());
    }
    
    vector<string> heat_csvs, position_files;
    for ( auto& project : all_projects )
    {
        heat_csvs.clear();
        position_files.clear();
        for (auto &p : filesystem::directory_iterator(project))
        {
            if (p.path().extension() == ".csv" && p.path().string().find("Heat") != string::npos)
            {
                std::cout << p.path().stem().string() << '\n';
                heat_csvs.push_back( p.path().string() );
            }
            if (p.path().extension() == ".csv" && p.path().string().find("gatesPosition") != string::npos)
            {
                std::cout << p.path().stem().string() << '\n';
                position_files.push_back( p.path().string() );
            }
        }
        
        if( position_files.size() != 1 )
        {
            cout<<"ERROR, position_files !=1 (gates position files)"<<endl;
            continue;
        }
        if( heat_csvs.size() < 1 )
        {
            cout<<"ERROR, heat_csvs <1 (heats files)"<<endl;
            continue;
        }
        
        vector<string> row;
        string myLine, word;
        rtree_type rtree;
        fstream filePositions( position_files[0], ios::in );
        getline( filePositions, myLine );
        cout<<myLine<<endl<<endl;
        while  ( getline( filePositions, myLine ) )
        {
            stringstream s( myLine );
            row.clear();
            while ( getline( s, word, ',' )) {
                row.push_back( word );
            }
//            cout<<"row:";
//            for ( auto & R : row )
//                cout<<R<<",";
//            cout<<endl;
            
            auto box_a = box_type{point_type{stod(row[1]),stod(row[2])}, point_type{stod(row[3]),stod(row[4])}};            
            rtree.insert(rtree_node_type{box_a, row[0]});
        }
        cout<<"position_files[0]"<<position_files[0]<<endl;
        
        std::map< std::string, double > gate_to_heat;
        
        for ( auto& heatFileName : heat_csvs )
        {
//            vector<boost::geometry::model::box<point_type> > all_heats;
//            all_heats.clear();
            fstream fHeat;
            gate_to_heat.clear();
            fHeat.close();
            fHeat.open( heatFileName, ios::in );
            std::vector<rtree_node_type> int_area_nodes;
            getline( fHeat, myLine );
            cout<<myLine<<endl<<endl;
            
            while  ( getline( fHeat, myLine ) )
            {
                stringstream s( myLine );
                row.clear();
                while ( getline( s, word, ',' )) {
                    row.push_back( word );
                }
                auto box_search = box_type{point_type{stod(row[0]),stod(row[1])}, point_type{stod(row[2]),stod(row[3])}};
                int_area_nodes.clear();
                rtree.query(boost::geometry::index::within(box_search), std::back_inserter(int_area_nodes));
                for ( auto& intersect : int_area_nodes )
                {
                    //if( gate_to_heat.find( intersect.second ) != gate_to_heat.end() )
                    gate_to_heat.insert( std::pair< std::string, double >( intersect.second, stod( row[4] ) ) );
                }
                //TODO remove gate position from rtree
            }
            std::cout << "heatFileName:" << heatFileName <<endl;
            std::string outName = heatFileName.erase( 0, heatFileName.find_last_of("/") );
            outName = outName.erase( outName.find_last_of("."), outName.size() );
            outName = project+outName+"_myOut.csv";
            std::cout << "outName:" << outName <<endl;
            fstream myOut( outName, ios::out );
            std::map< std::string, double >::iterator it;
            for( it = gate_to_heat.begin(); it != gate_to_heat.end(); ++it )
                myOut << it->first << "," << it->second << '\n';
        }
    }
    
    
    //show_rtree();
    return 0;
}

