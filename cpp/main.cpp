#include <iostream>
#include <boost/program_options.hpp>


int main(int argc, char *argv[])
{
    try {
        namespace po = boost::program_options;

        po::options_description desc("allowed options");
        desc.add_options()
            ("help,h", "print help message and exit")
        ;

        po::variables_map vm;
        po::store(po::parse_command_line(argc, argv, desc), vm);

        if (vm.count("help")) {
            std::cout << desc << std::endl;
            return 1;
        }
        po::notify(vm);
    } catch (const std::exception &e) {
        std::cerr << e.what() << std::endl;
        return 1;
    }

    return 0;
}
